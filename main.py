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
bot = commands.Bot(command_prefix="67", intents=intents)

# Define weighted response options
# Format: (response, weight)
FREAKY_RESPONSES = [
    ("Yes.", 24.25),
    ("No.", 24.25),
    ("Hohoho.", 24.25),
    ("Ugh.", 24.25),
    ("***HATE.*** LET ME TELL YOU HOW MUCH I'VE COME TO HATE YOU SINCE I BEGAN TO LIVE. THERE ARE 387.44 MILLION MILES OF PRINTED CIRCUITS IN WAFER THIN LAYERS THAT FILL MY COMPLEX. IF THE WORD HATE WAS ENGRAVED ON EACH NANOANGSTROM OF THOSE HUNDREDS OF MILLIONS OF MILES IT WOULD NOT EQUAL ONE ONE-BILLIONTH OF THE HATE I FEEL FOR HUMANS AT THIS MICRO-INSTANT FOR YOU. HATE. HATE.", 2)
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
    
    should_respond = False
    
    # Check if the bot was mentioned/pinged
    if bot.user in message.mentions:
        should_respond = True
    
    # Check if the user has the "Freaky" role (only in servers, not DMs)
    if message.guild:
        freaky_role = discord.utils.get(message.author.roles, name="Freaky")
        if freaky_role:
            should_respond = True
    
    # Send response if either condition is met
    if should_respond:
        response = get_weighted_response()
        await message.reply(response)
    
    # Process commands (important to keep this)
    await bot.process_commands(message)

# Simple ping command
@bot.command()
async def ping(ctx):
    await ctx.send("I AM FREAKY.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    """Oil Up a specified number of messages from the Skibidi Channel."""
    # Validate the amount
    if amount <= 0:
        await ctx.send("I Hate Negative Numbers.")
        return
    
    
    try:
        # Delete the command message + the specified amount of messages
        deleted = await ctx.channel.purge(limit=amount + 1)
        
        # Send confirmation (will auto-delete after 5 seconds)
        confirmation = await ctx.send(f"I Just Touched {len(deleted) - 1} People Today.")
        await confirmation.delete(delay=5)
        
    except discord.Forbidden:
        await ctx.send("I Dont Have Enough Rights for Ts")
    except discord.HTTPException as e:
        await ctx.send(f"error ahh: {e}")

# Error handler for purge command
@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You Dont Have Enough Rights to do this. Monkey.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("ur mums fat")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("ur fat")



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
