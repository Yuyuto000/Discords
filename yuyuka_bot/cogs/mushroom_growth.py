import discord
from discord.ext import commands, tasks
from discord import app_commands
import time
import random

class MushroomGrowthLoop(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_data = {}

    # きのこ育成の開始
    @app_commands.command(name="grow_mushroom",descripition="キノコをそだてよー！")
    async def grow_mushroom(self, ctx: discord.ApplicationContext):
        if ctx.author.id not in self.user_data:
            self.user_data[ctx.author.id] = {"growth_stage": 0, "last_grow_time": time.time()}
            await ctx.send("きのこを育てるよ！🌱成長を見守ってね！")
        else:
            await ctx.send("きのこは育て中！成長状態を見てみよう！")

    # きのこの状態を確認するコマンド
    @app_commands.command(name="check_mushroom",descripition="成長段階をみるよ！")
    async def check_mushroom(self, ctx: discord.ApplicationContext):
        if ctx.author.id not in self.user_data:
            await ctx.send("きのこを育てるために `/grow_mushroom` で育て始めてね！")
            return

        time_diff = time.time() - self.user_data[ctx.author.id]["last_grow_time"]
        growth_stage = int(time_diff // 60)  # 成長段階を分単位で計算

        if growth_stage > 5:
            growth_stage = 5  # 最大成長段階は5

        self.user_data[ctx.author.id]["growth_stage"] = growth_stage
        growth_stages = ["🌱", "🍄", "🍄🍄", "🍄🍄🍄", "🍄🍄🍄🍄", "🍄🍄🍄🍄🍄"]
        await ctx.send(f"あなたのきのこは現在: {growth_stages[growth_stage]}")

        # 最大成長段階に達したらリセット
        if growth_stage == 5:
            await ctx.send("おめでとう！きのこが最大成長したよ！次はもう一度最初から育てよう！")
            self.user_data[ctx.author.id]["growth_stage"] = 0
            self.user_data[ctx.author.id]["last_grow_time"] = time.time()

    # 定期的に成長を更新
    @tasks.loop(minutes=1)
    async def update_growth(self):
        for user_id, data in self.user_data.items():
            time_diff = time.time() - data["last_grow_time"]
            growth_stage = int(time_diff // 60)

            if growth_stage > 5:
                growth_stage = 5  # 最大成長段階
                self.user_data[user_id]["growth_stage"] = growth_stage
                self.user_data[user_id]["last_grow_time"] = time.time()  # リセット
                # 最大成長したらリセット
                self.user_data[user_id]["growth_stage"] = 0

# スラッシュコマンドをセットアップ
async def setup(bot: commands.Bot):
    await bot.add_cog(MushroomGrowthLoop(bot))
    await bot.tree.sync()
