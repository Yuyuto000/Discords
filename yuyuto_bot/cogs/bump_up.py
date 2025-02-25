import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio

class BumpUpNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bump", description="Bump通知を設定します。")
    async def bump(self, interaction: discord.Interaction, notify_role: discord.Role):
        """Bump通知を設定し、2時間後に自動で通知を送信します。"""
        embed = discord.Embed(
            title="Bump設定完了",
            description=f"2時間後にBump通知を送信します！\n通知対象: {notify_role.mention}",
            color=discord.Color.green()
        )
        embed.set_footer(text="Bump通知をお楽しみに！")
        await interaction.response.send_message(embed=embed)

        # 2時間（7200秒）後に通知
        await asyncio.sleep(7200)

        # 通知メッセージの作成
        bump_embed = discord.Embed(
            title="⏰ Bumpの時間です！",
            description=f"{notify_role.mention} さん、Bumpをする時間になりました！\n[ここをクリックしてBumpコマンドを実行してください](https://discord.com/channels/{interaction.guild_id}/{interaction.channel_id})",
            color=discord.Color.blue()
        )
        bump_embed.set_footer(text="忘れずにBumpしてください！")
        await interaction.channel.send(embed=bump_embed)

    @app_commands.command(name="up", description="Up通知を設定します。")
    async def up(self, interaction: discord.Interaction, notify_role: discord.Role):
        """Up通知を設定し、1時間後に自動で通知を送信します。"""
        embed = discord.Embed(
            title="Up設定完了",
            description=f"1時間後にUp通知を送信します！\n通知対象: {notify_role.mention}",
            color=discord.Color.orange()
        )
        embed.set_footer(text="Up通知をお楽しみに！")
        await interaction.response.send_message(embed=embed)

        # 1時間（3600秒）後に通知
        await asyncio.sleep(3600)

        # 通知メッセージの作成
        up_embed = discord.Embed(
            title="⏰ Upの時間です！",
            description=f"{notify_role.mention} さん、Upをする時間になりました！\n[ここをクリックしてUpコマンドを実行してください](https://discord.com/channels/{interaction.guild_id}/{interaction.channel_id})",
            color=discord.Color.purple()
        )
        up_embed.set_footer(text="忘れずにUpしてください！")
        await interaction.channel.send(embed=up_embed)

async def setup(bot):
    await bot.add_cog(BumpUpNotifier(bot))
