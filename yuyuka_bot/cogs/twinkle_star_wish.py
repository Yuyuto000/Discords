import discord
from discord.ext import commands
import random

class TwinkleStarWish(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="wish", help="星に願いを込めてみよう！")
    async def wish(self, ctx):
        wishes = [
            "⭐️「あなたの願いが叶いますように！」",
            "🌟「素敵な未来が待っています！」",
            "✨「きっと、幸せなことが起こるよ！」",
            "💫「信じて進めば、夢はきっとかなうよ！」"
        ]
        gifs = [
            "https://media.giphy.com/media/3o6nV78pKnKoHqmpay/giphy.gif",
            "https://media.giphy.com/media/MCjZty0t1fBv6/giphy.gif"
        ]

        wish_message = random.choice(wishes)
        gif = random.choice(gifs)

        await ctx.send(f"{wish_message}\n{gif}")

async def setup(bot: commands.Bot):
    await bot.add_cog(TwinkleStarWish(bot))
