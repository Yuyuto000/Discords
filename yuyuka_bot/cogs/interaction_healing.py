import discord
from discord.ext import commands
from discord import app_commands
import random

class InteractionHealing(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="inter_heal", description="リラックスしたい気分で癒しのメッセージをお届け🍃✨")
    async def inter_heal(self, interaction: discord.Interaction):
        messages = [
            "🌸「ゆっくり深呼吸してね、リラックスできるよ。」",
            "🍃「無理しないでね。心が穏やかになるように過ごしてね。」",
            "🌷「今この瞬間を楽しんで、焦らずいこうね。」"
        ]
        await interaction.response.send_message(random.choice(messages))

async def setup(bot: commands.Bot):
    await bot.add_cog(InteractionHealing(bot))
