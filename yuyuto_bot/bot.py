import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user}（イケメンBot）としてログインしました！")

    async def load_cogs():
        for filename in os.listdir("./yuyuto_bot/cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"yuyuto_bot.cogs.{filename[:-3]}")

                async def run_cool_bot():
                    await load_cogs()
    await bot.start("YOUR_COOL_BOT_TOKEN")