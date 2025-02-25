import discord
from discord.ext import commands, tasks
from discord import app_commands
import aiohttp
import json
import os

DATA_FILE = "area_data.json"
LAST_WEATHER_FILE = "last_weather_data.json"

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.area_data = self.load_area_data()
        self.last_weather_data = self.load_last_weather_data()
        self.weather_loop.start()

    def load_area_data(self):
        """エリアデータをファイルから読み込む"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_area_data(self):
        """エリアデータをファイルに保存"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.area_data, f, ensure_ascii=False, indent=4)

    def load_last_weather_data(self):
        """最後の気象データをファイルから読み込む"""
        if os.path.exists(LAST_WEATHER_FILE):
            with open(LAST_WEATHER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_last_weather_data(self):
        """最後の気象データをファイルに保存"""
        with open(LAST_WEATHER_FILE, "w", encoding="utf-8") as f:
            json.dump(self.last_weather_data, f, ensure_ascii=False, indent=4)

    async def fetch_weather_data(self, area_code: str):
        """指定されたエリアコードで気象情報を取得"""
        url = f"https://www.jma.go.jp/bosai/forecast/data/overview_forecast/{area_code}.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    @app_commands.command(name="set_area", description="気象情報エリアコードを選択し、気象情報を適格に送信します。")
    async def set_area(self, interaction: discord.Interaction):
        """エリアコードを設定し、Webhookを作成"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("⚠️ エリアコードを設定するには管理者権限が必要です。", ephemeral=True)
            return

        # エリアコードの選択肢を定義
        options = [
            discord.SelectOption(label="東京都", value="130000", description="東京都の気象情報"),
            discord.SelectOption(label="大阪府", value="270000", description="大阪府の気象情報"),
            discord.SelectOption(label="北海道", value="016000", description="北海道の気象情報"),
            discord.SelectOption(label="沖縄県", value="471000", description="沖縄県の気象情報")
        ]

        # 選択メニュー
        class AreaSelect(discord.ui.Select):
            def __init__(self, parent):
                super().__init__(placeholder="エリアコードを選択してください", options=options)
                self.parent = parent

            async def callback(self, interaction: discord.Interaction):
                guild_id = interaction.guild_id
                selected_area = self.values[0]

                # Webhook作成
                webhook = await self.create_webhook(interaction.channel, guild_id)

                # データ保存
                self.parent.area_data[guild_id] = {
                    "area_code": selected_area,
                    "webhook_url": webhook.url
                }
                self.parent.save_area_data()

                await interaction.response.send_message(
                    f"✅ エリアコード `{selected_area}` を設定し、専用Webhookを作成しました。",
                    ephemeral=True
                )

            async def create_webhook(self, channel, guild_id):
                """Webhookを作成または取得"""
                existing_webhooks = await channel.webhooks()
                for webhook in existing_webhooks:
                    if webhook.name == f"WeatherWebhook_{guild_id}":
                        return webhook
                return await channel.create_webhook(name=f"WeatherWebhook_{guild_id}")

        # ビューの定義
        class AreaSelectView(discord.ui.View):
            def __init__(self, parent):
                super().__init__()
                self.add_item(AreaSelect(parent))

        await interaction.response.send_message(
            "⚙️ 以下のメニューからエリアコードを選択してください。",
            view=AreaSelectView(self),
            ephemeral=True
        )

    @app_commands.command(name="update_area", description="既存のエリアコード設定を更新します。")
    async def update_area(self, interaction: discord.Interaction):
        """エリアコード設定を更新"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("⚠️ エリアコードを更新するには管理者権限が必要です。", ephemeral=True)
            return

        # エリアコードの選択肢を定義
        options = [
            discord.SelectOption(label="東京都", value="130000", description="東京都の気象情報"),
            discord.SelectOption(label="大阪府", value="270000", description="大阪府の気象情報"),
            discord.SelectOption(label="北海道", value="016000", description="北海道の気象情報"),
            discord.SelectOption(label="沖縄県", value="471000", description="沖縄県の気象情報")
        ]

        # 選択メニュー
        class AreaSelect(discord.ui.Select):
            def __init__(self, parent):
                super().__init__(placeholder="エリアコードを選択してください", options=options)
                self.parent = parent

            async def callback(self, interaction: discord.Interaction):
                guild_id = interaction.guild_id
                selected_area = self.values[0]

                # Webhookの取得・更新
                webhook = await self.update_webhook(interaction.channel, guild_id)

                # データ保存
                self.parent.area_data[guild_id] = {
                    "area_code": selected_area,
                    "webhook_url": webhook.url
                }
                self.parent.save_area_data()

                await interaction.response.send_message(
                    f"✅ エリアコード `{selected_area}` を更新し、Webhookを更新しました。",
                    ephemeral=True
                )

            async def update_webhook(self, channel, guild_id):
                """Webhookを更新または再作成"""
                existing_webhooks = await channel.webhooks()
                for webhook in existing_webhooks:
                    if webhook.name == f"WeatherWebhook_{guild_id}":
                        return webhook  # 既存のWebhookを再利用
                return await channel.create_webhook(name=f"WeatherWebhook_{guild_id}")

        # ビューの定義
        class AreaSelectView(discord.ui.View):
            def __init__(self, parent):
                super().__init__()
                self.add_item(AreaSelect(parent))

        await interaction.response.send_message(
            "⚙️ 以下のメニューから新しいエリアコードを選択してください。",
            view=AreaSelectView(self),
            ephemeral=True
        )

    @app_commands.command(name="reset_webhook", description="Webhookをリセットします。")
    async def reset_webhook(self, interaction: discord.Interaction):
        """Webhookをリセット"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("⚠️ Webhookをリセットするには管理者権限が必要です。", ephemeral=True)
            return

        guild_id = interaction.guild_id
        if guild_id not in self.area_data:
            await interaction.response.send_message("⚠️ このサーバーには設定されたWebhookがありません。", ephemeral=True)
            return

        # Webhook削除
        webhook_url = self.area_data[guild_id].get("webhook_url")
        async with aiohttp.ClientSession() as session:
            async with session.delete(webhook_url) as response:
                if response.status == 204:
                    del self.area_data[guild_id]
                    self.save_area_data()
                    await interaction.response.send_message("✅ Webhookをリセットしました。", ephemeral=True)
                else:
                    await interaction.response.send_message("⚠️ Webhookのリセットに失敗しました。", ephemeral=True)


    @tasks.loop(minutes=1)
    async def weather_loop(self):
        """1分ごとに気象情報を取得してWebhookに送信"""
        for guild_id, data in self.area_data.items():
            area_code = data["area_code"]
            webhook_url = data["webhook_url"]

            # 気象情報を取得
            weather_data = await self.fetch_weather_data(area_code)
            if not weather_data:
                print(f"⚠️ エリアコード {area_code} の気象情報取得に失敗しました。")
                continue

            # 重複投稿防止：最後に送信したデータと比較
            weather_text = weather_data.get("text", "")
            if guild_id in self.last_weather_data and self.last_weather_data[guild_id] == weather_text:
                print(f"🔄 重複データのため送信をスキップしました: Guild ID {guild_id}")
                continue

            # 埋め込みメッセージの作成
            embed = discord.Embed(
                title=f"気象情報 ({weather_data.get('publishingOffice', '不明')})",
                description=weather_data.get("headlineText", "情報なし"),
                color=discord.Color.blue()
            )
            embed.add_field(name="発表日時", value=weather_data.get("reportDatetime", "不明"), inline=False)
            embed.add_field(name="詳細情報", value=weather_text or "詳細情報がありません。", inline=False)
            embed.set_footer(text="提供: 気象庁 | JMA")

            # Webhookに送信
            async with aiohttp.ClientSession() as session:
                webhook_payload = {
                    "embeds": [embed.to_dict()]
                }
                async with session.post(webhook_url, json=webhook_payload) as response:
                    if response.status == 204:  # 成功
                        print(f"✅ Webhookに送信しました: Guild ID {guild_id}")
                        # 最後に送信したデータを更新
                        self.last_weather_data[guild_id] = weather_text
                        self.save_last_weather_data()
                    else:
                        print(f"⚠️ Webhook送信に失敗しました: Guild ID {guild_id}")

async def setup(bot):
    await bot.add_cog(WeatherCog(bot))
