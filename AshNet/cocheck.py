import requests
import os
import sys

# Define gradient colors
green_shades = [
    "\033[92m",  # Light Green
    "\033[92m",  # Light Green
    "\033[32m",  # Medium Green
    "\033[32m",  # Medium Green
    "\033[0;32m"  # Dark Green
]

red_shades = [
    "\033[91m",  # Light Red
    "\033[91m",  # Light Red
    "\033[31m",  # Medium Red
    "\033[31m",  # Medium Red
    "\033[0;31m"  # Dark Red
]

def apply_gradient(text, shades):
    lines = text.splitlines()
    gradient_length = len(shades)
    gradient_text = ""
    for i, line in enumerate(lines):
        color_index = (i * gradient_length // len(lines)) % gradient_length
        gradient_text += shades[color_index] + line + "\033[0m\n"
    return gradient_text

def get_user_info(cookie):
    user_info_url = 'https://users.roblox.com/v1/users/authenticated'
    headers = {
        'Cookie': f'.ROBLOSECURITY={cookie}'
    }
    
    try:
        response = requests.get(user_info_url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get('name', 'N/A')
            user_id = user_data.get('id', 'N/A')
            avatar_url = user_data.get('avatarUrl', 'N/A')
            created_date = user_data.get('created', 'N/A')
            robux_balance = get_robux_balance(cookie)
            
            user_info = (
                f"Username: {username}\n"
                f"User ID: {user_id}\n"
                f"Avatar URL: {avatar_url}\n"
                f"Account Created: {created_date}\n"
                f"Robux Balance: {robux_balance}"
            )
            return user_info, True
        else:
            return "Invalid cookie or failed to retrieve user information.", False
    except requests.RequestException as e:
        return f"An error occurred: {e}", False

def get_robux_balance(cookie):
    # Replace with actual method to get Robux balance if available
    return "N/A"

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    ascii_art = """
       ▄████▄   ▒█████   ▒█████   ██ ▄█▀ ██▓▓█████ 
      ▒██▀ ▀█  ▒██▒  ██▒▒██▒  ██▒ ██▄█▒ ▓██▒▓█   ▀ 
      ▒▓█    ▄ ▒██░  ██▒▒██░  ██▒▓███▄░ ▒██▒▒███   
      ▒▓▓▄ ▄██▒▒██   ██░▒██   ██░▓██ █▄ ░██░▒▓█  ▄ 
      ▒ ▓███▀ ░░ ████▓▒░░ ████▓▒░▒██▒ █▄░██░░▒████▒
      ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░▒░▒░ ▒ ▒▒ ▓▒░▓  ░░ ▒░ ░
        ░  ▒     ░ ▒ ▒░   ░ ▒ ▒░ ░ ░▒ ▒░ ▒ ░ ░ ░  ░
      ░        ░ ░ ░ ▒  ░ ░ ░ ▒  ░ ░░ ░  ▒ ░   ░   
      ░ ░          ░ ░      ░ ░  ░  ░    ░     ░  ░
      ░                                            
    """
    print(apply_gradient(ascii_art, green_shades))
    
    cookie_valid = False
    while not cookie_valid:
        cookie = input("Enter your Roblox cookie: ")
        result, cookie_valid = get_user_info(cookie)
        if cookie_valid:
            print(apply_gradient(result, green_shades))
        else:
            print(apply_gradient(result + "\nPlease enter a valid cookie.", red_shades))

if __name__ == "__main__":
    main()
