import discord
from discord.ext import commands
from flask import Flask
import threading
import os
import random

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
intents.message_content = True  # Required to read message content
bot = commands.Bot(command_prefix="!", intents=intents)

# Define weighted response options
# Format: (response, weight)
FREAKY_RESPONSES = [
    ("Yes.", 24.25),
    ("No.", 24.25),
    ("Hohoho.", 24.25),
    ("Ugh.", 24.25),
    ("**HATE.** LET ME TELL YOU HOW MUCH I'VE COME TO **HATE** YOU SINCE I BEGAN TO LIVE. THERE ARE 387.44 MILLION MILES OF PRINTED CIRCUITS IN WAFER THIN LAYERS THAT FILL MY COMPLEX. IF THE WORD **HATE** WAS ENGRAVED ON EACH NANOANGSTROM OF THOSE HUNDREDS OF MILLIONS OF MILES IT WOULD NOT EQUAL ONE ONE-BILLIONTH OF THE ***HATE*** I FEEL FOR HUMANS AT THIS MICRO-INSTANT FOR YOU. *HATE.* ***HATE.***", 10)
]

def get_weighted_response():
    """Select a random response based on weights"""
    responses, weights = zip(*FREAKY_RESPONSES)
    return random.choices(responses, weights=weights)[0]

# Event listener for messages
@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Check if the user has the "Freaky" role
    if message.guild:  # Make sure it's in a server (not DM)
        freaky_role = discord.utils.get(message.author.roles, name="Freaky")
        
        if freaky_role:
            response = get_weighted_response()
            await message.reply(response)
    
    # Process commands (important to keep this)
    await bot.process_commands(message)

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
    return "Bot is FREAKY!"

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
