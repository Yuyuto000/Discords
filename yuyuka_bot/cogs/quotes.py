import discord
from discord.ext import commands
from discord import app_commands
import random

class Quotes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="quote", description="ステキな名言を教えるよ！")
    async def quote(self, interaction: discord.Interaction):
        quotes = [
            "✨ 「夢を追いかけることが人生の魔法だよ！」 🦄💖",
            "🌈 「一歩踏み出せば、世界は広がる！」 🚀✨",
            "🐾 「小さな幸せを見つけること、それが大切だよ！」"
        ]
        await interaction.response.send_message(random.choice(quotes))

async def setup(bot: commands.Bot):
    await bot.add_cog(Quotes(bot))
    await bot.tree.sync()
