import discord
from discord.ext import commands
from discord import app_commands

class Mimic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ユーザーのメッセージをまねるスラッシュコマンド
    @app_commands.command(name="mimic", description="他のユーザーの言葉をまねします！")
    async def mimic(self, interaction: discord.Interaction, target: discord.Member, message: str):
        # メッセージをまねて返信
        await interaction.response.send_message(f"{target.mention} のまねっこ！: {message}")

# スラッシュコマンドをセットアップ
async def setup(bot: commands.Bot):
    await bot.add_cog(Mimic(bot))
    await bot.tree.sync()
