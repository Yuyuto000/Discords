import discord
from discord.ext import commands
from discord import app_commands

class UserInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="user_info", description="ユーザー情報を表示します。")
    async def user_info(self, interaction: discord.Interaction, user: discord.Member = None):
        """指定したユーザーの情報を表示します。指定がない場合はコマンド使用者の情報を表示します。"""
        user = user or interaction.user  # 引数が指定されない場合、コマンド使用者を対象に

        # アカウント作成日時とサーバー参加日時のフォーマット
        created_at = user.created_at.strftime("%Y/%m/%d %H:%M:%S")
        joined_at = user.joined_at.strftime("%Y/%m/%d %H:%M:%S") if user.joined_at else "不明"

        # ユーザーのステータスを取得
        status = str(user.status).capitalize()  # 例: "online" -> "Online"

        # ユーザー情報の埋め込みメッセージを作成
        embed = discord.Embed(
            title=f"{user.name} の情報",
            description=f"{user.mention} の詳細情報を表示します。",
            color=user.color
        )
        embed.set_thumbnail(url=user.avatar.url if user.avatar else None)  # ユーザーのアバター
        embed.add_field(name="ユーザー名", value=f"{user.name}#{user.discriminator}", inline=False)
        embed.add_field(name="ユーザーID", value=user.id, inline=False)
        embed.add_field(name="アカウント作成日", value=created_at, inline=False)
        embed.add_field(name="サーバー参加日", value=joined_at, inline=False)
        embed.add_field(name="ステータス", value=status, inline=False)
        embed.add_field(name="ロール", value=", ".join([role.mention for role in user.roles if role.name != "@everyone"]) or "なし", inline=False)
        embed.set_footer(text="ユーザー情報の表示です。")

        # 埋め込みメッセージを送信
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(UserInfoCog(bot))
