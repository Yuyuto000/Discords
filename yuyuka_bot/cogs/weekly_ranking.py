import discord
from discord.ext import commands, tasks
from collections import defaultdict
import time

class WeeklyRanking(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.rankings = defaultdict(int)  # ユーザーごとのスコアを保存
        self.last_reset = time.time()

    def reset_rankings(self):
        """週間ランキングリセット"""
        self.rankings = defaultdict(int)
        self.last_reset = time.time()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """メッセージを送るごとにスコアを加算"""
        if message.author.bot:
            return

        # メッセージごとにスコアを加算（仮に10点）
        self.rankings[message.author.id] += 10

    @commands.command(name="ranking", help="週間ランキングを表示します。")
    async def show_ranking(self, ctx: commands.Context):
        """ランキングを表示"""
        sorted_ranking = sorted(self.rankings.items(), key=lambda x: x[1], reverse=True)
        embed = discord.Embed(title="週間ランキング", color=discord.Color.blue())

        for rank, (user_id, score) in enumerate(sorted_ranking, 1):
            user = self.bot.get_user(user_id)
            embed.add_field(name=f"#{rank} {user.name}", value=f"スコア: {score}", inline=False)

        await ctx.send(embed=embed)

    @tasks.loop(hours=168)  # 168時間でリセット（1週間）
    async def reset_weekly_ranking(self):
        """1週間ごとにランキングリセット"""
        self.reset_rankings()

    @reset_weekly_ranking.before_loop
    async def before_reset_weekly_ranking(self):
        """最初にランタイムが開始されたときの処理"""
        print("週間ランキングのリセット準備中...")

async def setup(bot: commands.Bot):
    await bot.add_cog(WeeklyRanking(bot))
