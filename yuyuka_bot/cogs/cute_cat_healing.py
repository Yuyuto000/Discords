import discord
from discord.ext import commands
import random

class CuteCatHealing(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="cat_heal", help="癒しの猫ちゃんが登場！")
    async def cat_heal(self, ctx):
        healing_words = [
            "にゃんにゃん、あなたはとっても素敵な人だよ！😽",
            "にゃん！ゆっくり休んでね。癒されてね🐾",
            "わたしがずっとそばにいるから、安心してね！🐱",
            "にゃーん、あなたに良いことが訪れますように✨"
        ]
        gifs = [
            "https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif",
            "https://media.giphy.com/media/4pSndnN2akOTa/giphy.gif"
        ]
        
        heal_message = random.choice(healing_words)
        gif = random.choice(gifs)

        await ctx.send(f"{heal_message}\n{gif}")

async def setup(bot: commands.Bot):
    await bot.add_cog(CuteCatHealing(bot))
