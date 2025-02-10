import datetime
import discord
import os
from discord.ext import commands, tasks
import random
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# DEFINING TIME PERIODS

Gen = 1202305993954828292

MESSAGE_THRESHOLD = 150
MAX_SESSION_TIME_SECONDS = 10
TOKEN = "MTMzNzgwMjM4NDk0NDE0MDM4OA.GB7fm9.gGmAIvi-W6hxdfRJI0klRw1KQE4JMzsYy8SQQQ"
if TOKEN is None:
    raise ValueError(
        "TOKEN environment variable not set. Check your .env file.")
# ---------------------------------------------- #


@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0


#bot = commands.Bot(command_prefix='Nyxie, ', intents=discord.Intents.all())
bot = commands.Bot(command_prefix='Nyxie, ', intents=intents)
session = Session()


@bot.event
async def on_ready():
    global message_count
    message_count = 0
    print("Lets get it started")


@bot.command()
async def hello(ctx):  # test command to check if bot is working
    await ctx.send("Hello! I'm Nyxie, your friendly neighborhood bot! uwu")


@tasks.loop(seconds=MAX_SESSION_TIME_SECONDS, count=2)
async def break_reminder():
    if break_reminder.current_loop == 0:  # break reminder does not start immediately, but on second count
        return

    channel = bot.get_channel(Gen)
    await channel.send(
        f"# Time to take a break! You've been working for {MAX_SESSION_TIME_SECONDS} seconds. uwu"
    )


@bot.command()
async def add(ctx, *arr):  # command to calculate the sum of numbers
    result = 0
    for i in arr:
        result += int(i)
    await ctx.send(f"The total is {result}")


@bot.command()  # command to start an arbitrary session
async def start(ctx):
    if session.is_active:
        await ctx.send("Session is already active")
    else:
        session.is_active = True
        session.start_time = ctx.message.created_at.timestamp()
        human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
        break_reminder.start()
        await ctx.send(f"Session started at {human_readable_time} IST")


@bot.command()  # command to end the session
async def end(ctx):
    if not session.is_active:
        await ctx.send("Session not active!")
        return

    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    human_readable_end_time = ctx.message.created_at.strftime("%H:%M:%S")
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()
    await ctx.send(f"Session ended at {human_readable_end_time}.")
    await ctx.send(f"Session ended after {human_readable_duration}.")


@bot.command()
async def introduce(ctx):
    introduction_text = """Im Nyxie, the bot that exclusively caters to **The Attic™** discord server. Now technically, I am the successor to the late bot "SnapBot", but in reality, the only thing common between the two of us is the fact that we both are made from scratch by students studying commerce. Right now, the list of available commands is limited, but my creator (Dance) plans on adding exclusive commands, whenever he finds time to do so. Currently we are open to taking suggestions as to what kinda commands we should incorporate."""

    await ctx.send(introduction_text)

@bot.command()
async def lassi_dedo(ctx):
    lassi_text = """Lassi Menu

Classic Lassis

Sweet Lassi: ₹40
Salted Lassi: ₹45
Mango Lassi: ₹60
Strawberry Lassi: ₹60
Banana Lassi: ₹55
Specialty Lassis

Pistachio Lassi: ₹70
Almond Lassi: ₹70
Chocolate Lassi: ₹65
Coffee Lassi: ₹60
Mint Lassi: ₹55
Lassi with a Twist

Rose Lassi: ₹65
Saffron Lassi: ₹80
Cardamom Lassi: ₹55
Ginger Lassi: ₹55
Chili Lassi: ₹60
Lassi Floats

Mango Lassi Float: ₹80
Strawberry Lassi Float: ₹80
Chocolate Lassi Float: ₹75
Lassi Shakes

Mango Lassi Shake: ₹100
Strawberry Lassi Shake: ₹100
Chocolate Lassi Shake: ₹95
Lassi Extras

Add a flavor shot: +₹10
Add a topping: +₹15."""

    await ctx.send(lassi_text)


@bot.event
async def on_message(message):
    global message_count
    if message.author == bot.user:
        return
    
    if message.channel.id == Gen:
        message_count += 1
        print(f"Message received. Current count: {message_count}")

        if message_count >= MESSAGE_THRESHOLD:
            random_number = random.randint(-10000,10000)
            channel = bot.get_channel(Gen)
            await channel.send(f"{random_number} Aura Points")
            message_count = 0

    await bot.process_commands(message)
        
            


bot.run(TOKEN)
