import discord
from discord.ext import commands
from discord import app_commands

class ServerInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="server_info", description="サーバー情報を表示します。")
    async def server_info(self, interaction: discord.Interaction):
        guild = interaction.guild  # サーバー情報を取得

        # サーバーオーナーの取得
        owner = guild.owner

        # サーバー作成日時をフォーマット
        created_at = guild.created_at.strftime("%Y/%m/%d %H:%M:%S")

        # サーバー情報を埋め込み形式で表示
        embed = discord.Embed(
            title=f"{guild.name} の情報",
            description="サーバーの詳細情報を以下に表示します。",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)  # サーバーのアイコン
        embed.add_field(name="サーバー名", value=guild.name, inline=False)
        embed.add_field(name="サーバーID", value=guild.id, inline=False)
        embed.add_field(name="サーバー作成日", value=created_at, inline=False)
        embed.add_field(name="サーバーオーナー", value=owner.mention if owner else "不明", inline=False)
        embed.add_field(name="メンバー数", value=f"{guild.member_count} 人", inline=False)
        embed.add_field(name="ブーストレベル", value=f"レベル {guild.premium_tier}", inline=False)
        embed.add_field(name="ブースト数", value=f"{guild.premium_subscription_count} 回", inline=False)
        embed.add_field(name="チャンネル数", value=f"{len(guild.channels)} 個", inline=False)
        embed.set_footer(text="サーバー情報を表示しています。")

        # メッセージ送信
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerInfoCog(bot))
