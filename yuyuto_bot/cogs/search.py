import discord
from discord.ext import commands
from discord import app_commands
import requests
import json

# Google Custom Search APIキーとCSE ID
API_KEY = "YOUR_API_KEY"  # ここにAPIキーを入力
CSE_ID = "YOUR_CSE_ID"  # ここにCSE IDを入力


class GoogleSearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def google_search(self, query):
        """Google Custom Searchを実行して、検索結果を取得"""
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CSE_ID}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Google APIエラー: {response.status_code}")
            return []
        search_results = response.json()
        return search_results.get("items", [])

    @commands.Cog.listener()
    async def on_message(self, message):
        """「〇〇とは」「〇〇って？」形式のメッセージに反応し、リアクションを付与"""
        if message.author.bot:
            return

        # メッセージが指定フォーマットに一致する場合
        if message.content.endswith("とは") or message.content.endswith("って？"):
            await message.add_reaction("🔍️")  # 🔍️リアクションを追加

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """リアクションが追加された際にGoogle検索を実行"""
        if user.bot:
            return

        # リアクションが 🔍️ かつ、メッセージのフォーマットが正しい場合
        if reaction.emoji == "🔍️" and reaction.message.content.endswith(("とは", "って？")):
            query = reaction.message.content.replace("とは", "").replace("って？", "").strip()
            search_results = self.google_search(query)

            if not search_results:
                await reaction.message.channel.send(f"🔍️ `{query}` に関する検索結果は見つかりませんでした。")
                return

            # 検索結果を埋め込み形式で送信
            embed = discord.Embed(
                title=f"検索結果: {query}",
                description="以下の結果が見つかりました。",
                color=discord.Color.blue()
            )

            for idx, result in enumerate(search_results[:7]):  # 最大7件表示
                embed.add_field(
                    name=f"{idx + 1}. {result['title']}",
                    value=f"[リンク]({result['link']})",
                    inline=False
                )

            await reaction.message.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(GoogleSearchCog(bot))
