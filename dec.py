import os
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import csv

# GLOBAL CONSTANT
CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State" % (os.environ['USERPROFILE']))
CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data" % (os.environ['USERPROFILE']))

def get_secret_key():
    try:
        #(1) Get secretkey from chrome local state
        with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        # Remove suffix DPAPI
        secret_key = secret_key[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        print("%s" % str(e))
        print("[ERR] Chrome secretkey cannot be found")
        return None
    
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        #(3-a) Initialisation vector for AES decryption
        initialisation_vector = ciphertext[3:15]
        #(3-b) Get encrypted password by removing suffix bytes (last 16 bits)
        # Encrypted password is 192 bits
        encrypted_password = ciphertext[15:-16]
        #(4) Build the cipher to decrypt the ciphertext
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  
        return decrypted_pass
    except Exception as e:
        print("%s" % str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""
    
def get_db_connection(chrome_path_login_db):
    try:
        print(chrome_path_login_db)
        shutil.copy2(chrome_path_login_db, "Loginvault.db") 
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print("%s" % str(e))
        print("[ERR] Chrome database cannot be found")
        return None

if __name__ == '__main__':
    try:
        # List all folders (profiles) under the Chrome User Data folder, including custom profiles
        profiles = [folder for folder in os.listdir(CHROME_PATH) if os.path.isdir(os.path.join(CHROME_PATH, folder))]
        # Filter out profiles that do not contain a Login Data file
        valid_profiles = [folder for folder in profiles if os.path.exists(os.path.join(CHROME_PATH, folder, 'Login Data'))]
        
        if not valid_profiles:
            print("[ERR] No valid profiles with 'Login Data' file found.")
            exit()

        print("Available profiles with saved passwords:", valid_profiles)
        
        # Ask the user to choose which profile to extract passwords from
        target_profile = input("Please enter the profile name from which you want to extract passwords: ")

        # Check if the selected profile exists
        if target_profile not in valid_profiles:
            print(f"[ERR] The profile '{target_profile}' does not exist or does not have a 'Login Data' file.")
        else:
            # Create DataFrame to store passwords
            with open('decrypted_password.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
                csv_writer = csv.writer(decrypt_password_file, delimiter=',')
                csv_writer.writerow(["index", "url", "username", "password"])

                #(1) Get secret key
                secret_key = get_secret_key()

                # Construct the path to the Login Data database for the specified profile
                chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (CHROME_PATH, target_profile))

                if os.path.exists(chrome_path_login_db):
                    conn = get_db_connection(chrome_path_login_db)
                    if secret_key and conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                        for index, login in enumerate(cursor.fetchall()):
                            url = login[0]
                            username = login[1]
                            ciphertext = login[2]
                            if url != "" and username != "" and ciphertext != "":
                                #(3) Filter the initialisation vector & encrypted password from ciphertext 
                                #(4) Use AES algorithm to decrypt the password
                                decrypted_password = decrypt_password(ciphertext, secret_key)
                                print("Sequence: %d" % (index))
                                print("URL: %s\nUser Name: %s\nPassword: %s\n" % (url, username, decrypted_password))
                                print("*" * 50)
                                #(5) Save into CSV 
                                csv_writer.writerow([index, url, username, decrypted_password])
                        # Close database connection
                        cursor.close()
                        conn.close()
                        # Delete temp login db
                        os.remove("Loginvault.db")
                else:
                    print(f"[ERR] Profile '{target_profile}' does not have a Login Data file.")
    except Exception as e:
        print("[ERR] %s" % str(e))
