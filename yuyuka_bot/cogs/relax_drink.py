import discord
from discord.ext import commands
from discord import app_commands
import random

class RelaxDrink(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="relax_drink", description="今飲むと癒される飲み物を提案するよ☕✨")
    async def relax_drink(self, interaction: discord.Interaction):
        drinks = [
            "☕ 温かいココアを飲んで、ほっとしよう♪",
            "🍵 ハーブティーでリラックスしよっ🌿",
            "🥛 ホットミルクでぬくぬくしちゃお♪"
        ]
        await interaction.response.send_message(random.choice(drinks))

async def setup(bot: commands.Bot):
    await bot.add_cog(RelaxDrink(bot))
