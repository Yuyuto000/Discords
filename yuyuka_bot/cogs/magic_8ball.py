import discord
from discord.ext import commands
from discord import app_commands
import random

class Magic8Ball(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="8ball", description="ふしぎな8ボールがあなたの質問に答えるよ🎱✨")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        responses = [
            "うん！絶対に大丈夫！🐰💖", "ぜったいそうにゃん！😺✨", 
            "んー… ちょっとわからないにゃ 🤔", "ごめんね、それはナイショだよ！🙈💭"
        ]
        await interaction.response.send_message(f"🎱 **質問:** {question}\n✨ **答え:** {random.choice(responses)}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Magic8Ball(bot))
