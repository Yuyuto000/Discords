import discord
from discord.ext import commands
from discord import app_commands
import random

class HealingBGM(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="bgm", description="癒しのBGMをおすすめするよ🎶")
    async def bgm(self, interaction: discord.Interaction):
        bgm_list = [
            "🌿 **ヒーリングピアノ** → https://www.youtube.com/watch?v=eR5oP6u1UlA",
            "🌊 **波の音でリラックス** → https://www.youtube.com/watch?v=3aH2JgNLpAw",
            "🔥 **焚き火の音でまったり** → https://www.youtube.com/watch?v=VXvT8FuFqUo"
        ]
        await interaction.response.send_message(random.choice(bgm_list))

async def setup(bot: commands.Bot):
    await bot.add_cog(HealingBGM(bot))
