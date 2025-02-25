import discord
from discord.ext import commands
from discord import app_commands

class Stamp(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # スタンプ風のメッセージを作成するコマンド
    @app_commands.command(name="stamp", description="スタンプ風のメッセージを作成します！")
    async def stamp(self, interaction: discord.Interaction, message: str):
        # メッセージをスタンプ風に加工
        stamped_message = f"🦄✨ {message} ✨🦄"
        await interaction.response.send_message(stamped_message)

# スラッシュコマンドをセットアップ
async def setup(bot: commands.Bot):
    await bot.add_cog(Stamp(bot))
    await bot.tree.sync()
