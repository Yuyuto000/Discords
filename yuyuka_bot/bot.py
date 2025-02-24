import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user}（可愛い癒しBot）としてログインしました！")

    async def load_cogs():
        for filename in os.listdir("./cute_bot/cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cute_bot.cogs.{filename[:-3]}")

                async def run_cute_bot():
                    await load_cogs()
    await bot.start("YOUR_CUTE_BOT_TOKEN")