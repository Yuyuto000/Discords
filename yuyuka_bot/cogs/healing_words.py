import discord
from discord.ext import commands
from discord import app_commands
import random

class HealingWords(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="healing", description="癒しのことばをお届けするよ🍃✨")
    async def healing(self, interaction: discord.Interaction):
        messages = [
            "🌸「ゆっくり深呼吸してね、きっと大丈夫だよ。」",
            "🌿「無理しすぎないでね、あなたは素敵な人だよ。」",
            "☁️「疲れたら、お空を見上げてひとやすみ♪」"
        ]
        await interaction.response.send_message(random.choice(messages))

async def setup(bot: commands.Bot):
    await bot.add_cog(HealingWords(bot))
