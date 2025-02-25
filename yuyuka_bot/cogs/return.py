import discord
from discord.ext import commands
import random

class ResponseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # あらかじめ定義した言葉と返信のマッピング
        self.responses = {
            "こんにちは": [
                "こんにちは！元気ですか？",
                "やあ、こんにちは！"
            ],
            "お疲れ様": [
                "お疲れ様です！ゆっくり休んでね。",
                "今日もお疲れ様でした！"
            ],
            "ありがとう": [
                "どういたしまして！",
                "感謝の気持ちを伝えられて嬉しいです！"
            ],
            "さようなら": "またね！気をつけて！",
            "HELP": "どういったことを手伝いましょうか？質問してね！"
        }

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 自分のボットが送ったメッセージには反応しない
        if message.author == self.bot.user:
            return

        # 部分一致でメッセージを確認
        for keyword, reply in self.responses.items():
            if keyword.lower() in message.content.lower():  # 部分一致を小文字で比較
                # 複数の返答候補がある場合、ランダムに選んで返答
                if isinstance(reply, list):
                    response = random.choice(reply)
                else:
                    response = reply
                
                # 返答メッセージを送信
                await message.channel.send(response)
                break  # 一度マッチしたら他のキーワードはチェックしない

# ボットの初期化
async def setup(bot):
    await bot.add_cog(ResponseCog(bot))
