import discord
from discord.ext import commands
from discord import app_commands
import random

class RelaxTips(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="relax", description="リラックスする方法を教えるよ✨")
    async def relax(self, interaction: discord.Interaction):
        tips = [
            "🛁「ゆっくりお風呂につかって、ぽかぽかしよう♪」",
            "🧸「お気に入りのぬいぐるみをギュッと抱きしめよう💖」",
            "🌿「やさしい音楽を聴いて、心を落ち着けてみてね♪」"
        ]
        await interaction.response.send_message(random.choice(tips))

async def setup(bot: commands.Bot):
    await bot.add_cog(RelaxTips(bot))
