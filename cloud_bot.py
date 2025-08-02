import discord
from discord.ext import commands, tasks
import random
import asyncio
import json
import os
from datetime import datetime, time
import aiohttp
from dotenv import load_dotenv

# Load environment variables (works both locally and on Railway)
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='~', intents=intents, help_command=None)

# Cozy data for the bot
COZY_RESPONSES = [
    "🌸 Hello there, lovely soul! How can I make your day more cozy?",
    "✨ Welcome to my little corner of warmth and comfort!",
    "🌺 *wraps you in a virtual blanket* What brings you here today?",
    "🍃 Take a deep breath... you're in a safe, cozy space now.",
    "🌙 Whether it's day or night, there's always time for comfort."
]

AFFIRMATIONS = [
    "🌸 You are enough, exactly as you are right now.",
    "✨ Your presence makes the world a little brighter.",
    "🌺 You deserve all the love and kindness you give to others.",
    "🍃 Every small step you take is progress worth celebrating.",
    "🌙 You have survived 100% of your difficult days so far.",
    "🌻 Your feelings are valid, and it's okay to take things slowly.",
    "🌸 You bring something special to this world that no one else can."
]

COMFORT_MESSAGES = [
    "🫖 *brews you a warm cup of chamomile tea* Everything will be okay.",
    "🌸 *offers a soft blanket* You're safe here. Take all the time you need.",
    "✨ *lights a gentle candle* This too shall pass, dear one.",
    "🌺 *sends warm hugs* You're stronger than you know.",
    "🍃 *creates a cozy reading nook* Rest here as long as you need."
]

@bot.event
async def on_ready():
    print(f'🌸 LazyBot has awakened in their cozy cottage! 🏠')
    print(f'✨ Connected as {bot.user} ✨')
    print(f'🌿 Serving {len(bot.guilds)} cozy server(s)')
    
    # Set cozy status
    activities = [
        "🌸 brewing chamomile tea",
        "✨ reading by the fireplace",
        "🌺 tending to the garden",
        "🍃 knitting cozy blankets",
        "🌙 watching the stars"
    ]
    activity = discord.Activity(type=discord.ActivityType.custom, name=random.choice(activities))
    await bot.change_presence(activity=activity)
    
    # Start daily affirmations
    if not daily_affirmation.is_running():
        daily_affirmation.start()

@bot.event
async def on_member_join(member):
    """Welcome new members with cozy vibes"""
    welcome_messages = [
        f"🌸 Welcome to our cozy corner, {member.mention}! *offers warm tea* ✨",
        f"✨ A new friend has arrived! Welcome, {member.mention}! 🌺",
        f"🌻 {member.mention} has joined our little cottage! Make yourself at home! 🏠"
    ]
    
    # Try to send to system channel or first available channel
    channel = member.guild.system_channel
    if not channel:
        channel = next((ch for ch in member.guild.text_channels if ch.permissions_for(member.guild.me).send_messages), None)
    
    if channel:
        await channel.send(random.choice(welcome_messages))

@bot.command(name='help')
async def help_command(ctx):
    """Show all cozy commands"""
    embed = discord.Embed(
        title="🌸 LazyBot's Cozy Commands 🌸",
        description="*Welcome to your digital cottage of comfort*",
        color=0xFFB6C1
    )
    
    embed.add_field(
        name="🌺 Comfort Commands",
        value="`~affirmation` - Daily gentle affirmation\n`~comfort` - Receive cozy comfort\n`~hug` - Get a warm virtual hug",
        inline=False
    )
    
    embed.add_field(
        name="✨ Fun Commands",
        value="`~tea` - Get a warm drink recipe\n`~story` - Hear a cozy bedtime story\n`~quote` - Inspirational quote",
        inline=False
    )
    
    embed.add_field(
        name="🌙 Interaction",
        value="Mention me (@LazyBot) for natural conversation!\nI'm here to chat and spread cozy vibes 💕",
        inline=False
    )
    
    embed.set_footer(text="🍃 Made with love and chamomile tea")
    await ctx.send(embed=embed)

@bot.command(name='affirmation')
async def affirmation(ctx):
    """Send a gentle daily affirmation"""
    embed = discord.Embed(
        title="🌸 Daily Affirmation 🌸",
        description=random.choice(AFFIRMATIONS),
        color=0xFFB6C1
    )
    embed.set_footer(text="✨ You are loved and valued")
    await ctx.send(embed=embed)

@bot.command(name='comfort')
async def comfort(ctx):
    """Provide cozy comfort"""
    embed = discord.Embed(
        title="🫖 Cozy Comfort Corner 🫖",
        description=random.choice(COMFORT_MESSAGES),
        color=0xDDA0DD
    )
    embed.set_footer(text="🌙 Take your time, you're safe here")
    await ctx.send(embed=embed)

@bot.command(name='hug')
async def hug(ctx):
    """Give a warm virtual hug"""
    hugs = [
        f"🤗 *gives {ctx.author.mention} the warmest, coziest hug* 💕",
        f"🌸 *wraps {ctx.author.mention} in a soft, lavender-scented embrace* ✨",
        f"💝 *sends {ctx.author.mention} a hug filled with sunshine and kindness* 🌻"
    ]
    await ctx.send(random.choice(hugs))

@bot.command(name='tea')
async def tea_recipe(ctx):
    """Share a warm drink recipe"""
    recipes = [
        "🫖 **Chamomile Dreams**: Steep chamomile flowers with honey and a dash of vanilla. Perfect for peaceful evenings! 🌙",
        "☕ **Cozy Cocoa**: Warm milk with cocoa powder, cinnamon, and marshmallows. Add a pinch of love! 💕",
        "🍃 **Mint Serenity**: Fresh mint leaves in hot water with lemon and honey. Refreshing and calming! ✨",
        "🌸 **Lavender Latte**: Steamed milk with lavender syrup and a gentle coffee base. Aromatic bliss! 💜"
    ]
    
    embed = discord.Embed(
        title="🍵 Cozy Drink Recipe 🍵",
        description=random.choice(recipes),
        color=0x98FB98
    )
    embed.set_footer(text="🌺 Made with love in LazyBot's kitchen")
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    """Check bot responsiveness"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🌸 Pong! *{latency}ms* - I'm here and cozy! ✨")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Process commands first
    await bot.process_commands(message)
    
    # Respond to mentions
    if bot.user in message.mentions and not message.content.startswith('~'):
        response = random.choice(COZY_RESPONSES)
        await message.reply(response)

@tasks.loop(time=time(9, 0))  # 9 AM daily
async def daily_affirmation():
    """Send daily affirmations to all servers"""
    for guild in bot.guilds:
        # Find a suitable channel
        channel = guild.system_channel
        if not channel:
            channel = next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages), None)
        
        if channel:
            embed = discord.Embed(
                title="🌅 Good Morning Affirmation 🌅",
                description=random.choice(AFFIRMATIONS),
                color=0xFFD700
            )
            embed.set_footer(text="✨ Starting your day with love and positivity")
            try:
                await channel.send(embed=embed)
            except:
                pass  # Skip if can't send

@daily_affirmation.before_loop
async def before_daily_affirmation():
    await bot.wait_until_ready()

if __name__ == "__main__":
    # Get token from environment variable
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    
    if not TOKEN:
        print("❌ No DISCORD_BOT_TOKEN found in environment variables!")
        print("🌸 Please set your bot token in the environment variables")
        exit(1)
    
    print("🌿 Starting LazyBot for cloud deployment...")
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid bot token! Please check your DISCORD_BOT_TOKEN")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")