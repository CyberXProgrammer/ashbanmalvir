import os
from colorama import init, Fore, Style

init(autoreset=True)

def run_script(script_name):
    try:
        script_path = os.path.join(script_name)
        if os.path.exists(script_path):
            exec(open(script_path).read())
        else:
            print(f"{Fore.RED}Script {script_name} not found.")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}")

def main():
    print(f"{Fore.GREEN}Choose a brute force method:")
    print(f"{Fore.GREEN}1. SSH Brute Force")
    print(f"{Fore.GREEN}2. HTTP Basic Auth Brute Force")
    print(f"{Fore.GREEN}3. Something Brute Force")
    print(f"{Fore.GREEN}4. Something Brute Force")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        run_script('force/ssh/ssh.py')
    elif choice == '2':
        run_script('force/http_auth/http_auth.py')
    elif choice == '3':
        run_script('force/other1/other1.py')  # Placeholder
    elif choice == '4':
        run_script('force/other2/other2.py')  # Placeholder
    else:
        print(f"{Fore.RED}Invalid choice, please select a number between 1 and 4.")

if __name__ == "__main__":
    main()
