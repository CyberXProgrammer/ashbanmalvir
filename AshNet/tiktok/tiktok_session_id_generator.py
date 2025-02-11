import random
import string

def generate_hex_session_id(length=32):
    # Define the characters for base-16 encoding
    hex_chars = string.ascii_lowercase[:6] + string.digits
    return ''.join(random.choices(hex_chars, k=length))

def main():
    generated_ids = set()
    
    while True:
        session_id = generate_hex_session_id()
        if session_id not in generated_ids:
            generated_ids.add(session_id)
            with open("ids.txt", "a") as file:
                file.write(session_id + "\n")
            print(f"Generated and saved session ID: {session_id}")
        else:
            print(f"Duplicate session ID detected: {session_id}")

if __name__ == "__main__":
    main()
