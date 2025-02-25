import discord
from discord.ext import commands
from discord import app_commands

class TriggerReplyHealing(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # ユーザーが「しんどい」と言ったら
        if "しんどい" in message.content.lower():
            await message.channel.send("🍃「無理しないでね。ゆっくり休んでね。おつかれさま。」")
        
        # ユーザーが「ありがとう」と言ったら
        elif "ありがとう" in message.content:
            await message.channel.send("💖「どういたしまして！あなたの笑顔が一番嬉しいよ！」")

async def setup(bot: commands.Bot):
    await bot.add_cog(TriggerReplyHealing(bot))
