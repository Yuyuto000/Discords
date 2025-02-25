import discord
from discord.ext import commands
import random

class ResponseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # あらかじめ定義した言葉と返信のマッピング
        self.responses = {
            "こんにちは": [
                "(∩´∀｀)∩やっほぉ！どうしたの？",
                "|ω・｀)ﾉ ﾔｧ、こんにちは！"
            ],
            "疲れた": [
                "💖「少し休んでね、あなたは頑張ってるよ！」",
                "💛「無理しないでね！」",
                "🌸「お疲れ様！ゆっくり休んでね🍃」",
                "💖「頑張ったね！リラックスしようね！」",
                "🍵「少しお茶を飲んで、元気を取り戻してね☕」",
                "🍃「無理しないでね。ゆっくり休んでね。おつかれさま。」"
            ],
            "ありがとう": [
                "🌸「どういたしまして！いつでもあなたの味方だよ！」",
                "🌺「(∀｀*ゞ)ｴﾍﾍ」",
                "💖「どういたしまして！あなたの笑顔が一番嬉しいよ！」"
            ],
            "寝れない|ねれない": [
                "💤「スマホを遠くに置いて、心を落ち着けてみてね。」"
                "🌙「お気に入りの枕で、ふわふわの夢を見よう！」"
                "🛌「寝る前にあたたかいミルクを飲むと、リラックスできるよ☕✨」"
            ],
            "助けて": "どうしたの？大丈夫(・・?"
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
    await bot.tree.sync()
