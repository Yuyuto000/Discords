import discord
from discord.ext import commands

class CasualConversation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if "こんにちは" in message.content:
            await message.channel.send("🐾「こんにちは！今日もがんばろうね！」")
        elif "お疲れ様" in message.content:
            await message.channel.send("🌸「お疲れ様！リラックスしてね🍃」")

async def setup(bot: commands.Bot):
    await bot.add_cog(CasualConversation(bot))
    await bot.tree.sync()
