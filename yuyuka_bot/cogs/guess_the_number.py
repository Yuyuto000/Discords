import discord
from discord.ext import commands
import random

class GuessTheNumber(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="guess", help="数字当てゲーム！1〜100の間で数字を当ててね！")
    async def guess(self, ctx):
        number = random.randint(1, 100)
        await ctx.send("数字当てゲーム！1から100の間で数字を予想してね！")

        def check(msg):
            return msg.author == ctx.author and msg.content.isdigit()

        try:
            while True:
                user_guess = await self.bot.wait_for('message', check=check, timeout=30)
                user_guess = int(user_guess.content)

                if user_guess < number:
                    await ctx.send("もっと大きな数字だよ！")
                elif user_guess > number:
                    await ctx.send("もっと小さな数字だよ！")
                else:
                    await ctx.send(f"おめでとう！正解は {number} だよ！🎉")
                    break
        except TimeoutError:
            await ctx.send("時間切れ！また遊んでね💖")

async def setup(bot: commands.Bot):
    await bot.add_cog(GuessTheNumber(bot))
    await bot.tree.sync()
