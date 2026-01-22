import discord
from discord.ext import commands
from flask import Flask
import threading
import os

# ------------------------------
# Discord Bot Setup
# ------------------------------

# Use your bot token as an environment variable for safety
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_TOKEN = DISCORD_TOKEN.strip()
if not DISCORD_TOKEN:
    raise ValueError("Please set the DISCORD_TOKEN environment variable!")

# Create bot instance
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Simple ping command
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

# ------------------------------
# Flask App for uptime ping
# ------------------------------

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run_flask():
    # Run on the port Render assigns (or 10000 as default)
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ------------------------------
# Run both Discord bot and Flask
# ------------------------------
print(DISCORD_TOKEN)
if __name__ == "__main__":
    # Start Flask in a background thread
    threading.Thread(target=run_flask, daemon=True).start()
    # Start Discord bot (blocking call)
    bot.run(DISCORD_TOKEN)
