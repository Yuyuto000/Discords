import discord
from discord.ext import commands
import random

class GoodNight(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="goodnight", help="おやすみなさいのメッセージを送るよ💤")
    async def goodnight(self, ctx):
        messages = [
            "💤おやすみなさい！素敵な夢を見てね🌙",
            "✨ゆっくり休んで、明日も元気にね！おやすみなさい💖",
            "🌟眠る時間だよ、夢の世界へと旅立とう！おやすみ〜💫",
            "🌜おやすみなさい、夢の中で会おうね！💤"
        ]
        gifs = [
            "https://media.giphy.com/media/1nA0bSYZgYts4/giphy.gif",
            "https://media.giphy.com/media/TlKepZXA7Y4tW/giphy.gif"
        ]

        message = random.choice(messages)
        gif = random.choice(gifs)

        await ctx.send(f"{message}\n{gif}")

async def setup(bot: commands.Bot):
    await bot.add_cog(GoodNight(bot))
