import discord
from discord import app_commands
import random

# おみくじの結果リスト（自由にカスタマイズ可能）
OMIKUJI_RESULTS = [
    "大吉: 素晴らしい一日が待ってるよ❤",
    "中吉: 良いことが起こる予感！",
    "小吉: 少しの幸運があなたを待ってるよ",
    "末吉: これから良くなりそう！",
    "吉: 平和な一日を過ごせそう。",
    "凶: 気を付けて！見守ってるから！",
]

class OmikujiCog(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # スラッシュコマンドを登録
    @app_commands.command(name="omikuji", description="あなたの今日を占うよ❤")
    async def omikuji(self, interaction: discord.Interaction):
        # ランダムにおみくじ結果を選択
        result = random.choice(OMIKUJI_RESULTS)

        # 埋め込みメッセージを作成
        embed = discord.Embed(
            title="🎋 今日のおみくじ 🎋",
            description=f"あなたのおみくじ結果: **{result}**",
            color=discord.Color.green()
        )
        embed.set_footer(text="❤良い一日になりますよーに❤")

        # 結果を送信
        await interaction.response.send_message(embed=embed)

    # コマンドツリーに登録
    async def cog_load(self):
        self.bot.tree.add_command(self.omikuji)

    async def cog_unload(self):
        self.bot.tree.remove_command(self.omikuji.name)

# ボットでロードする際のエントリーポイント
async def setup(bot):
    await bot.add_cog(OmikujiCog(bot))
