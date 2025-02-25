import discord
from discord.ext import commands
import json
import os

class DMSettings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.settings_file = 'user_settings.json'

        # 設定ファイルがなければ作成
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, 'w') as f:
                json.dump({}, f)

    async def send_dm(self, user: discord.User, message: str):
        try:
            await user.send(message)
        except discord.Forbidden:
            await user.send("DMを送信できませんでした。設定を反映させるにはDMを許可してください。")

    @commands.command(name="set_message", help="あなたの「おやすみメッセージ」を設定します")
    async def set_message(self, ctx: commands.Context, *, message: str):
        # ユーザー設定をファイルに保存
        user_id = str(ctx.author.id)
        with open(self.settings_file, 'r') as f:
            settings = json.load(f)

        if user_id not in settings:
            settings[user_id] = {}

        settings[user_id]['goodnight_message'] = message

        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)

        await ctx.send("おやすみメッセージが設定されました！💤")

    @commands.command(name="get_message", help="あなたの「おやすみメッセージ」を表示します")
    async def get_message(self, ctx: commands.Context):
        # ユーザー設定をファイルから取得
        user_id = str(ctx.author.id)
        with open(self.settings_file, 'r') as f:
            settings = json.load(f)

        if user_id in settings and 'goodnight_message' in settings[user_id]:
            message = settings[user_id]['goodnight_message']
            await ctx.send(f"あなたのおやすみメッセージは: {message}💤")
        else:
            await ctx.send("設定されていません。`!set_message`で設定してください。")

    @commands.command(name="send_goodnight_dm", help="設定されたおやすみメッセージをDMで送ります")
    async def send_goodnight_dm(self, ctx: commands.Context):
        user_id = str(ctx.author.id)
        with open(self.settings_file, 'r') as f:
            settings = json.load(f)

        if user_id in settings and 'goodnight_message' in settings[user_id]:
            message = settings[user_id]['goodnight_message']
            await self.send_dm(ctx.author, f"おやすみなさい！{message}💖")
        else:
            await ctx.send("おやすみメッセージが設定されていません。`!set_message`で設定してください。")

    @commands.command(name="set_favorite_character", help="お気に入りのキャラクターを設定します")
    async def set_favorite_character(self, ctx: commands.Context, *, character_name: str):
        user_id = str(ctx.author.id)
        with open(self.settings_file, 'r') as f:
            settings = json.load(f)

        if user_id not in settings:
            settings[user_id] = {}

        settings[user_id]['favorite_character'] = character_name

        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)

        await ctx.send(f"お気に入りのキャラクター「{character_name}」が設定されました！✨")

    @commands.command(name="get_favorite_character", help="お気に入りのキャラクターを表示します")
    async def get_favorite_character(self, ctx: commands.Context):
        user_id = str(ctx.author.id)
        with open(self.settings_file, 'r') as f:
            settings = json.load(f)

        if user_id in settings and 'favorite_character' in settings[user_id]:
            character_name = settings[user_id]['favorite_character']
            await ctx.send(f"あなたのお気に入りキャラクターは: {character_name}🎉")
        else:
            await ctx.send("お気に入りキャラクターが設定されていません。`!set_favorite_character`で設定してください。")

async def setup(bot: commands.Bot):
    await bot.add_cog(DMSettings(bot))
