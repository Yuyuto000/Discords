import discord
from discord.ext import commands
from discord import app_commands
import requests

class CatBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="cat", description="可愛い猫の画像をランダムで送ります！")
    async def cat(self, interaction: discord.Interaction):
        # 猫の画像を取得するAPI
        url = "https://api.thecatapi.com/v1/images/search"
        response = requests.get(url)
        data = response.json()
        image_url = data[0]["url"]
        
        await interaction.user.send(f"🐱 あなたにかわいい猫をお届け！\n{image_url}")
        await interaction.response.send_message("猫の画像をDMで送ったよ！🐾", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(CatBot(bot))
