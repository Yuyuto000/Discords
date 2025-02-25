import discord
from discord.ext import commands, tasks
from discord import app_commands
import requests
import json
from discord.ui import Button, View
from datetime import datetime

class EarthquakeNotifier(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.webhook_url = None  # Webhook URL 初期化

    # 管理者コマンド：Webhookを設定
    @app_commands.command(name="set_earthquake",descripitions="地震情報送信チャンネルを設定します。")
    @commands.has_permissions(administrator=True)
    async def set_webhook(self, ctx: discord.ApplicationContext, url: str):
        """WebHookを設定するコマンド"""
        self.webhook_url = url
        await ctx.send(f"地震速報のWebhookが設定されました！")

    # 管理者コマンド：Webhook解除
    @app_commands.command(name="remove_earthquake",descripitions="地震速報のチャンネルを解除します。")
    @commands.has_permissions(administrator=True)
    async def remove_webhook(self, ctx: discord.ApplicationContext):
        """Webhookを解除するコマンド"""
        self.webhook_url = None
        await ctx.send("地震速報のWebhookが解除されました。")

    # 地震速報を取得し、Webhookを使って通知
    @tasks.loop(minutes=1.0)
    async def fetch_earthquake_info(self):
        if not self.webhook_url:
            return  # Webhook URLが設定されていない場合、通知はしない

        # USGS Earthquake API (ここでは最新の地震情報を取得)
        api_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()

            # 最新の地震情報を取得
            if data['features']:
                latest_earthquake = data['features'][0]
                magnitude = latest_earthquake['properties']['mag']
                place = latest_earthquake['properties']['place']
                time = latest_earthquake['properties']['time']
                time = datetime.utcfromtimestamp(time / 1000).strftime('%Y-%m-%d %H:%M:%S')

                # 地震情報が強い場合、Webhookに送信
                if magnitude >= 3.0:  # 任意のしきい値
                    message = f"🚨 **地震速報** 🚨\n" \
                              f"**場所**: {place}\n" \
                              f"**規模**: {magnitude} M\n" \
                              f"**時間**: {time}\n" \
                              f"詳細: [USGS Link](https://earthquake.usgs.gov/earthquakes/eventpage/{latest_earthquake['id']})"

                    # Webhook送信
                    webhook_data = {
                        "content": message,
                        "username": "地震速報Bot",
                    }

                    try:
                        requests.post(self.webhook_url, json=webhook_data)
                    except Exception as e:
                        print(f"Webhook送信エラー: {e}")

    # Cogが読み込まれた際にタスクを開始
    @commands.Cog.listener()
    async def on_ready(self):
        self.fetch_earthquake_info.start()

# Cogのセットアップ
async def setup(bot: commands.Bot):
    await bot.add_cog(EarthquakeNotifier(bot))
    await bot.tree.sync()
