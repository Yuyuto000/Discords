import discord
from discord.ext import commands

class KeywordTrigger(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        keywords = ["疲れた", "しんどい", "癒し", "ありがとう"]
        
        # メッセージにキーワードが含まれている場合
        if any(keyword in message.content for keyword in keywords):
            if "疲れた" in message.content or "しんどい" in message.content:
                await message.channel.send("💖「少し休んでね、あなたは頑張ってるよ！」")
            elif "ありがとう" in message.content:
                await message.channel.send("🌸「どういたしまして！いつでもあなたの味方だよ！」")

async def setup(bot: commands.Bot):
    await bot.add_cog(KeywordTrigger(bot))
