import discord
from discord.ext import commands
from discord import app_commands
import os

# Botの設定
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 権限エラーの処理
async def send_permission_error(interaction: discord.Interaction, error_message: str):
    embed = discord.Embed(
        title="権限エラー",
        description=error_message,
        color=discord.Color.red()
    )
    embed.set_footer(text="Botの権限を確認してください。")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await send_permission_error(
            interaction,
            "このコマンドを実行するには管理者権限が必要です。"
        )
    elif isinstance(error, discord.app_commands.BotMissingPermissions):
        missing_perms = ', '.join(error.missing_permissions)
        await send_permission_error(
            interaction,
            f"Botに次の権限が不足しています: {missing_perms}"
        )
    else:
        embed = discord.Embed(
            title="エラーが発生しました",
            description="予期しないエラーが発生しました。開発者にお問い合わせください。",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.event
async def on_ready():
    print(f"{bot.user}（癒しBot）としてログインしました！")

async def load_cogs():
    for filename in os.listdir("./yuyuka_bot/cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"yuyuka_bot.cogs.{filename[:-3]}")

async def run_cute_bot():
    await load_cogs()
    await bot.start("YOUR_CUTE_BOT_TOKEN")
