import discord
from discord.ext import commands
from datetime import datetime, timezone
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

GTA6_RELEASE = datetime(2026, 11, 19, 0, 0, 0, tzinfo=timezone.utc)

class MyBot(commands.Bot):
    async def setup_hook(self):
        self.loop.create_task(update_status())

bot = MyBot(command_prefix="!", intents=intents)

async def update_status():
    await bot.wait_until_ready()

    while not bot.is_closed():
        now = datetime.now(timezone.utc)
        delta = GTA6_RELEASE - now

        if delta.total_seconds() <= 0:
            status_text = "Launched!"
        else:
            days = delta.days
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            status_text = f"{days}d {hours}h {minutes}m"

        activity = discord.Game(name=status_text)
        await bot.change_presence(activity=activity)

        print(f"Status updated to: {status_text}")

        await asyncio.sleep(60)

@bot.event
async def on_ready():
    try:
        await bot.user.edit(username="GTA VI Countdown")
        print("Bot username set to GTA VI Countdown")
    except Exception as e:
        print(f"Username update skipped: {e}")

    print(f"Bot is online as {bot.user}")

@bot.command()
async def gta6(ctx):
    now = datetime.now(timezone.utc)
    delta = GTA6_RELEASE - now

    if delta.total_seconds() <= 0:
        await ctx.send("GTA 6 is available now")
        return

    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = delta.seconds % 60

    await ctx.send(
        f"GTA 6 releases in {days} days {hours} hours {minutes} minutes {seconds} seconds"
    )

token = os.getenv("DISCORD_TOKEN")
bot.run(token)
