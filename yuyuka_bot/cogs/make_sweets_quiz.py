import discord
from discord.ext import commands
import random

class MakeSweetsQuiz(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="sweets_quiz", help="スイーツクイズに挑戦！")
    async def sweets_quiz(self, ctx):
        sweets = [
            ("マカロン", "フランスの色とりどりなスイーツ"),
            ("カップケーキ", "カップ型のケーキ"),
            ("タルト", "フルーツが乗ったおしゃれなスイーツ"),
            ("ドーナツ", "丸い形の甘いお菓子")
        ]

        sweet, hint = random.choice(sweets)

        await ctx.send(f"ヒント: {hint}\nこのスイーツの名前は何でしょうか？")

        def check(msg):
            return msg.author == ctx.author and msg.content.lower() == sweet.lower()

        try:
            user_answer = await self.bot.wait_for('message', check=check, timeout=30)
            await ctx.send(f"おめでとう！正解は【{sweet}】でした！🎉")
        except:
            await ctx.send(f"残念！正解は【{sweet}】でした！また挑戦してね🍰")

async def setup(bot: commands.Bot):
    await bot.add_cog(MakeSweetsQuiz(bot))
    await bot.tree.sync()
