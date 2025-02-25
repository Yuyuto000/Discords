import discord
from discord.ext import commands
from discord import app_commands
import random

class Dice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="dice", description="サイコロを振ってみよう🎲")
    async def dice(self, interaction: discord.Interaction):
        roll = random.randint(1, 6)
        await interaction.response.send_message(f"🎲 サイコロの出た目は **{roll}** だよ！✨")

async def setup(bot: commands.Bot):
    await bot.add_cog(Dice(bot))
    await bot.tree.sync()
