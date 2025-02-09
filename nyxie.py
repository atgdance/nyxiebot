
import datetime
import discord
import os
from discord.ext import commands, tasks
import random
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv(dotenv_path=r"C:\Users\admin\Documents\Discord_bot\.env")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)    
message_counts = {}

# DEFINING TIME PERIODS 

Gen = 1337803837603450882
MAX_SESSION_TIME_SECONDS = 10

TOKEN = os.getenv("TOKEN")
if TOKEN is None: 
     raise ValueError("TOKEN environment variable not set. Check your .env file.")
# ---------------------------------------------- #

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix='Nyxie,', intents =discord.Intents.all())
session = Session()

@bot.event
async def on_ready():
    print("Lets get it started")
    channel = bot.get_channel(Gen) 
    await channel.send("I'm here to help you uwu")

@bot.command()
async def hello(ctx):                                                                           # test command to check if bot is working
    await ctx.send("Hello! I'm Nyxie, your friendly neighborhood bot! uwu")

@tasks.loop(seconds=MAX_SESSION_TIME_SECONDS, count=2)  
async def break_reminder():
    if break_reminder.current_loop == 0:                                                        # break reminder does not start immediately, but on second count
        return

    channel = bot.get_channel(Gen)
    await channel.send(f"# Time to take a break! You've been working for {MAX_SESSION_TIME_SECONDS} seconds. uwu")

@bot.command()
async def bruh(ctx, *arr):                                                                         # command to calculate the sum of numbers                            
    result = 0
    for i in arr:
        result += int(i)        
    await ctx.send(f"The total is {result}")

@bot.command()                                                                                 # command to start an arbitrary session                  
async def start(ctx):
    if session.is_active:
        await ctx.send("Session is already active")
    else:
        session.is_active = True
        session.start_time = ctx.message.created_at.timestamp()
        human_readable_time =  ctx.message.created_at.strftime("%H:%M:%S")
        break_reminder.start()
        await ctx.send(f"Session started at {human_readable_time} IST")

@bot.command()                                                                                  # command to end the session
async def end(ctx):
    if not session.is_active:
        await ctx.send("Session not active!")
        return

    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    human_readable_end_time =  ctx.message.created_at.strftime("%H:%M:%S")
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()
    await ctx.send(f"Session ended at {human_readable_end_time}.")
    await ctx.send(f"Session ended after {human_readable_duration}.")












bot.run(TOKEN)