import discord
from discord.ext import commands
from discord import app_commands
import random

class SleepTips(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sleep", description="ぐっすり眠れるアドバイスをするよ💤")
    async def sleep(self, interaction: discord.Interaction):
        tips = [
            "💤「スマホを遠くに置いて、心を落ち着けてみてね。」",
            "🌙「お気に入りの枕で、ふわふわの夢を見よう！」",
            "🛌「寝る前にあたたかいミルクを飲むと、リラックスできるよ☕✨」"
        ]
        await interaction.response.send_message(random.choice(tips))

async def setup(bot: commands.Bot):
    await bot.add_cog(SleepTips(bot))
