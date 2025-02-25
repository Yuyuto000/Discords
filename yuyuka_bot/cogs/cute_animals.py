import discord
from discord.ext import commands
from discord import app_commands
import random

class CuteAnimals(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cute", description="もふもふな動物画像をお届けするよ！🐾")
    async def cute(self, interaction: discord.Interaction):
        images = [
            "https://placekitten.com/400/400",  # かわいい子猫
            "https://placedog.net/400",         # わんちゃん
            "https://www.placetotoro.com/400"   # 架空のかわいい動物（例）
        ]
        await interaction.response.send_message(random.choice(images))

async def setup(bot: commands.Bot):
    await bot.add_cog(CuteAnimals(bot))
