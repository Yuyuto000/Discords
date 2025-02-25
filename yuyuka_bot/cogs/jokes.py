import discord
from discord.ext import commands
from discord import app_commands
import random

class Jokes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="joke", description="ランダムなかわいいジョークをお届け♪")
    async def joke(self, interaction: discord.Interaction):
        jokes = [
            "どうして猫ちゃんはパソコンの上に座るの？\n\n→ **「Ctrl」を手に入れるためだにゃ！** 🐱",
            "チーズがドレッシングをかけたらどうなる？\n\n→ **「チーズドレッシング」！🧀✨**",
            "ひよこが一番好きなお茶はなに？\n\n→ **「ぴよぴよ（ピーチ）ティー！」🐣🍑**"
        ]
        await interaction.response.send_message(random.choice(jokes))

async def setup(bot: commands.Bot):
    await bot.add_cog(Jokes(bot))
    await bot.tree.sync()
