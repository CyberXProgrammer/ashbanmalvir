import os
import sys
import subprocess
from colorama import init, Style, Fore

init(autoreset=True)

green_shades = [
    "\033[38;5;82m",  # Light green
    "\033[38;5;118m", # Medium green
    "\033[38;5;154m", # Bright green
    "\033[38;5;190m", # Light yellow-green
    "\033[38;5;46m",  # Greenish
    "\033[38;5;40m",  # Deep green
    "\033[38;5;34m",  # Dark green
    "\033[38;5;28m",  # Very dark green
    "\033[38;5;22m"   # Darkest green
]

def apply_gradient(text, gradient):
    lines = text.split('\n')
    gradient_length = len(gradient)
    if gradient_length == 0:
        raise ValueError("Gradient length must be greater than zero.")
    
    num_lines = len(lines)
    gradient_step = num_lines // gradient_length if num_lines >= gradient_length else 1

    result = ""
    for i, line in enumerate(lines):
        color_index = min(i // gradient_step, gradient_length - 1)
        result += gradient[color_index] + line + Style.RESET_ALL + '\n'
    
    return result

def center_text(text, terminal_width):
    """Center the text in the terminal."""
    lines = text.split('\n')
    centered_lines = [line.center(terminal_width) for line in lines]
    return '\n'.join(centered_lines)

def format_features(features, gradient):
    gradient_length = len(gradient)
    formatted_features = ""
    for i, feature in enumerate(features):
        color_index = i % gradient_length
        formatted_features += gradient[color_index] + f"{i+1}. {feature}" + Style.RESET_ALL + '\n'
    return formatted_features

def gradient_input(prompt, gradient):
    """Generate a gradient input prompt."""
    gradient_length = len(gradient)
    formatted_prompt = ""
    for i in range(len(prompt)):
        color_index = i % gradient_length
        formatted_prompt += gradient[color_index] + prompt[i]
    return formatted_prompt + Style.RESET_ALL

def run_program(option):
    programs = {
        1: "gen.py",
        2: "cocheck.py",
        3: "tiktok/tiktok_session_id_checker.py",
        4: "tiktok/tiktok_session_id_generator.py",
        5: "logger/log.py",
        6: "ddos/ddos.py",
        7: "adb/adb.py"
    }
    program = programs.get(option)
    if program and os.path.isfile(program):
        os.system(f"python {program}")
    else:
        print(Fore.RED + "Error: The program file does not exist.")

def brute_force_menu():
    print(Fore.GREEN + "1. HTTP AUTH\n2. SSH")
    while True:
        try:
            choice = int(input(Fore.GREEN + "Your Choice> " + Style.RESET_ALL))
            if choice == 1:
                if os.path.isfile("force/http_auth/http_auth.py"):
                    os.system("python force/http_auth/http_auth.py")
                else:
                    print(Fore.RED + "Error: HTTP AUTH script does not exist.")
                break
            elif choice == 2:
                if os.path.isfile("force/ssh/ssh.py"):
                    os.system("python force/ssh/ssh.py")
                else:
                    print(Fore.RED + "Error: SSH script does not exist.")
                break
            else:
                print(Fore.RED + "Invalid choice. Please choose 1 or 2.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter 1 or 2.")

def main():
    ascii_art = """
        ▄████████    ▄████████    ▄█    █▄    ███▄▄▄▄      ▄████████     ███     
       ███    ███   ███    ███   ███    ███   ███▀▀▀██▄   ███    ███ ▀█████████▄ 
       ███    ███   ███    █▀    ███    ███   ███   ███   ███    █▀     ▀███▀▀██ 
      ███    ███   ███         ▄███▄▄▄▄███▄▄ ███   ███  ▄███▄▄▄         ███   ▀ 
    ▀███████████ ▀███████████ ▀▀███▀▀▀▀███▀  ███   ███ ▀▀███▀▀▀         ███     
      ███    ███          ███   ███    ███   ███   ███   ███    █▄      ███     
      ███    ███    ▄█    ███   ███    ███   ███   ███   ███    ███     ███     
      ███    █▀   ▄████████▀    ███    █▀     ▀█   █▀    ██████████    ▄████▀   
    """

    features = [
        "Roblox Cookie Generator",
        "Cookie Checker",
        "TikTok Session ID Checker",
        "TikTok Session ID Generator",
        "Image-Logger",
        "DDoS Attack",
        "ADB Exploit",
        "Brute-Force",
        "Exit"
    ]

    terminal_width = os.get_terminal_size().columns
    gradient_text = apply_gradient(ascii_art, green_shades)
    centered_ascii = center_text(gradient_text, terminal_width)
    gradient_features = format_features(features, green_shades)
    centered_features = center_text(gradient_features, terminal_width)

    print(centered_ascii)
    print(centered_features)

    # Get the username from the whoami command
    username = subprocess.check_output("whoami").decode().strip().split('\\')[-1]  # Extract only the username

    # Create the gradient prompt with a box-like structure
    top_line = f"┌──────[{username}]"
    bottom_line = "└────────> $ "

    # Apply gradient to the top and bottom line
    gradient_top = gradient_input(top_line, green_shades)
    gradient_bottom = gradient_input(bottom_line, green_shades)

    print(gradient_top)
    print(gradient_bottom, end='')  # Prevent newline after printing the bottom prompt

    # Wait for user input on the same line as the prompt
    choice = input()  # No space; this will take input directly after the prompt

    while True:
        try:
            choice = int(choice)  # Convert input to integer
            if 1 <= choice <= 9:
                if choice == 8:
                    brute_force_menu()
                elif choice == 9:
                    print(Fore.RED + "Exiting...")
                    sys.exit()
                else:
                    run_program(choice)
            else:
                print(Fore.RED + "Invalid choice. Exiting...")
                sys.exit()
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()
