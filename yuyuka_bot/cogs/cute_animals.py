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
            "https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif",  # かわいい猫
            "https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif",  # もふもふ犬
            "https://media.giphy.com/media/4Zo41lhzKt6iZ8xff9/giphy.gif"  # ぴょこぴょこウサギ
        ]
        await interaction.response.send_message(random.choice(images))

async def setup(bot: commands.Bot):
    await bot.add_cog(CuteAnimals(bot))
