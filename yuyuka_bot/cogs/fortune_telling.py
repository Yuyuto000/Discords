import discord
from discord.ext import commands
from discord import app_commands
import random

class FortuneTelling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 占いの結果をランダムに返すコマンド
    @app_commands.command(name="fortune", description="キラキラ占いだよ✨")
    async def fortune(self, interaction: discord.Interaction):
        fortunes = [
            "✨今日も素敵な1日になる予感✨",
            "🌸少し努力すれば、素晴らしいことが待っているよ！🌸",
            "💫今日はあなたにとって幸運の1日💫",
            "🌈ちょっとした冒険が待っているかも！🌈",
            "🍀ゆっくりリラックスすると良いことが起きるよ🍀",
            "🎉大切な人と素敵な時間を過ごせる予感🎉"
        ]
        fortune = random.choice(fortunes)
        await interaction.response.send_message(f"🔮占いの結果: {fortune}")

# スラッシュコマンドをセットアップ
async def setup(bot: commands.Bot):
    await bot.add_cog(FortuneTelling(bot))
    await bot.tree.sync()
