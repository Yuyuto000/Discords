import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime
import json

class DMSettings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.users_data = {}
        self.load_data()

    # 設定ファイルを読み込む
    def load_data(self):
        try:
            with open("dm_settings.json", "r") as f:
                self.users_data = json.load(f)
        except FileNotFoundError:
            self.users_data = {}

    # 設定ファイルを保存する
    def save_data(self):
        with open("dm_settings.json", "w") as f:
            json.dump(self.users_data, f, indent=4)

    # おやすみメッセージの送信時刻を設定するスラッシュコマンド
    @app_commands.command(name="set_goodnight", description="おやすみメッセージの送信時刻を設定します。")
    async def set_goodnight(self, interaction: discord.Interaction, time: str):
        # 時間のフォーマットを検証
        try:
            time_obj = datetime.strptime(time, "%H:%M").time()
        except ValueError:
            await interaction.response.send_message("時間の形式が正しくありません。例: 23:00 のように指定してください。", ephemeral=True)
            return

        # ユーザーの設定データを保持
        if interaction.user.id not in self.users_data:
            self.users_data[interaction.user.id] = {}

        self.users_data[interaction.user.id]["goodnight"] = str(time_obj)
        self.save_data()

        await interaction.response.send_message(f"おやすみメッセージの送信時刻を{time_obj}に設定しました。", ephemeral=True)

    # 誕生日メッセージの送信時刻を設定するスラッシュコマンド
    @app_commands.command(name="set_birthday", description="誕生日メッセージの送信時刻を設定します。")
    async def set_birthday(self, interaction: discord.Interaction, date: str):
        # 日付のフォーマットを検証
        try:
            date_obj = datetime.strptime(date, "%m-%d").date()
        except ValueError:
            await interaction.response.send_message("日付の形式が正しくありません。例: 05-01 のように指定してください。", ephemeral=True)
            return

        # ユーザーの設定データを保持
        if interaction.user.id not in self.users_data:
            self.users_data[interaction.user.id] = {}

        self.users_data[interaction.user.id]["birthday"] = str(date_obj)
        self.save_data()

        await interaction.response.send_message(f"誕生日メッセージの送信日を{date_obj}に設定しました。", ephemeral=True)

    # おやすみメッセージを送るタスク
    @tasks.loop(minutes=1)
    async def send_goodnight_dm(self):
        current_time = datetime.now().strftime("%H:%M")

        # おやすみメッセージを設定しているユーザーに送信
        for user_id, settings in self.users_data.items():
            if "goodnight" in settings and settings["goodnight"] == current_time:
                user = self.bot.get_user(user_id)
                if user:
                    await user.send(f"💤 おやすみなさい！素敵な夢を見てね！🌙")
    
    # 誕生日メッセージを送るタスク
    @tasks.loop(hours=24)
    async def send_birthday_dm(self):
        current_date = datetime.now().strftime("%m-%d")

        # 誕生日メッセージを設定しているユーザーに送信
        for user_id, settings in self.users_data.items():
            if "birthday" in settings:
                birthday_date = settings["birthday"]
                if current_date == birthday_date:
                    user = self.bot.get_user(user_id)
                    if user:
                        await user.send(f"🎉お誕生日おめでとう！🎂素敵な一日を過ごしてね！🎈")
    
    # Bot起動時にタスクを開始
    @commands.Cog.listener()
    async def on_ready(self):
        self.send_goodnight_dm.start()
        self.send_birthday_dm.start()

# スラッシュコマンドをセットアップ
async def setup(bot: commands.Bot):
    await bot.add_cog(DMSettings(bot))
    # スラッシュコマンドを同期
    await bot.tree.sync()
