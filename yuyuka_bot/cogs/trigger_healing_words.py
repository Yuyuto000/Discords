import discord
from discord.ext import commands
from discord import app_commands
import random

class TriggerHealingWords(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 特定のワードをトリガーに癒しのメッセージ
        if "疲れた" in message.content:
            messages = [
                "🌸「お疲れ様！ゆっくり休んでね🍃」",
                "💖「頑張ったね！リラックスしようね！」",
                "🍵「少しお茶を飲んで、元気を取り戻してね☕」"
            ]
            await message.channel.send(random.choice(messages))

async def setup(bot: commands.Bot):
    await bot.add_cog(TriggerHealingWords(bot))
