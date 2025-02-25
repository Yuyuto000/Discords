import discord
from discord.ext import commands
from discord import app_commands
import random

class CandyGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_data = {}

    # ゲームを始めるコマンド
    @app_commands.command(name="start_candy_game",description="キャンディーゲームを始めるよ💛")
    async def start_candy_game(self, ctx: discord.ApplicationContext):
        if ctx.author.id not in self.user_data:
            self.user_data[ctx.author.id] = {"candies": 0}
            await ctx.send("お菓子集めが始まりました！🍬どれくらい集められるか挑戦してみてね！")
        else:
            await ctx.send("すでにお菓子集めを始めているよ！次の結果を見てみよう！")

    # お菓子を集めるコマンド
    @app_commands.command(name="collect_candy",description="お菓子を集めよう！")
    async def collect_candy(self, ctx: discord.ApplicationContext):
        if ctx.author.id not in self.user_data:
            await ctx.send("ゲームがまだ始まっていません！`/start_candy_game` で始めてね！")
            return

        # ランダムにお菓子を集める
        candies_found = random.randint(1, 5)
        self.user_data[ctx.author.id]["candies"] += candies_found
        await ctx.send(f"お菓子を {candies_found} 個集めたよ！現在のお菓子の数は: {self.user_data[ctx.author.id]['candies']} 個！")

    # ゲームの結果を確認するコマンド
    @app_commands.command(name="check_candy",descripton="集めた結果を見るよ！")
    async def check_candy(self, ctx: discord.ApplicationContext):
        if ctx.author.id not in self.user_data:
            await ctx.send("ゲームがまだ始まっていません！`/start_candy_game` で始めてね！")
            return

        await ctx.send(f"現在あなたが集めたお菓子の数は: {self.user_data[ctx.author.id]['candies']} 個だよ！")

# スラッシュコマンドをセットアップ
async def setup(bot: commands.Bot):
    await bot.add_cog(CandyGame(bot))
    await bot.tree.sync()
