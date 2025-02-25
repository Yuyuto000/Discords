import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta


class DayChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_channels = {}  # チャンネルIDをキーにして終了時間を保存

    @app_commands.command(name="daychat", description="1日限定のチャットを作成します。")
    async def daychat(self, interaction: discord.Interaction):
        # チャンネルの初期化（24時間固定）
        channel_id = interaction.channel_id
        now = datetime.now(datetime.timezone.utc)
        end_time = now + timedelta(hours=24)
        self.active_channels[channel_id] = end_time

        # 初期化メッセージをEmbed形式で送信
        embed = discord.Embed(
            title="1Dayチャットの初期化完了",
            description=(
                "このチャンネルは1日限定のチャットとして設定されました。\n"
                f"⏰ **終了予定時刻**: {end_time.strftime('%Y-%m-%d %H:%M:%S UTC')}"
            ),
            color=discord.Color.green(),
        )
        embed.set_footer(text="24時間後に自動的に期限が切れます。")
        await interaction.response.send_message(embed=embed)
        await interaction.channel.send(
            "✅ このチャンネルは1日限定のチャットとして設定されました！\n"
            "有効期限が過ぎると終了通知が送信されます。"
        )

        # チャンネルを監視して期限切れになったら通知
        await self.handle_channel_lifetime(interaction.channel, end_time)

    async def handle_channel_lifetime(self, channel, end_time):
        # 指定された時間まで待機
        remaining_time = (end_time - datetime.utcnow()).total_seconds()
        if remaining_time > 0:
            await asyncio.sleep(remaining_time)

        # 期限切れ時の処理
        await channel.send(
            "https://tenor.com/ja/view/kaboom-explosion-disaster-explode-gif-17774478"
        )

    @app_commands.command(name="enddaychat", description="1Dayチャットを手動で終了します。")
    async def enddaychat(self, interaction: discord.Interaction):
        channel_id = interaction.channel_id
        if channel_id in self.active_channels:
            del self.active_channels[channel_id]  # チャンネルをリストから削除

            # 終了通知をEmbed形式で送信
            embed = discord.Embed(
                title="1Dayチャットの手動終了",
                description="このチャンネルの1Dayチャットを手動で終了しました。",
                color=discord.Color.orange(),
            )
            embed.set_footer(text="以後、このチャンネルは通常のチャットとして利用できます。")
            await interaction.response.send_message(embed=embed)

            await interaction.channel.send(
                "🎆 https://tenor.com/ja/view/kaboom-explosion-disaster-explode-gif-17774478"
            )
        else:
            # 1Dayチャットが設定されていない場合のエラー応答
            embed = discord.Embed(
                title="⚠️ エラー",
                description="このチャンネルは現在1Dayチャットとして設定されていません。",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(DayChatCog(bot))
