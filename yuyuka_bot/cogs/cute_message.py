import discord
from discord.ext import commands
from discord import app_commands
import random

class CuteMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="love", description="かわいいメッセージを送るよ💖")
    async def love(self, interaction: discord.Interaction):
        messages = [
            "🌸 あなたはとっても素敵だよ！", "💖 今日も笑顔でいてね！", "🐰 みんなあなたのこと大好き！"
        ]
        await interaction.response.send_message(random.choice(messages))

async def setup(bot: commands.Bot):
    await bot.add_cog(CuteMessage(bot))
    await bot.tree.sync()
