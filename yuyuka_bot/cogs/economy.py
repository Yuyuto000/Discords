import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random

DATA_FILE = "yuyuka_bot/data/bot_users.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

class EconomyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.data = load_data()

    def update_user(self, user_id: str):
        if user_id not in self.data:
        # 初期状態：100コイン、レベル1、XP0
            self.data[user_id] = {"balance": 100, "level": 1, "xp": 0}
            save_data(self.data)

@app_commands.command(name="balance", description="自分の所持コインを確認します。")
async def balance(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        self.update_user(user_id)
        balance = self.data[user_id]["balance"]
        await interaction.response.send_message(f"{interaction.user.mention} さんの所持コインは **{balance}** コインです！")

@app_commands.command(name="earn", description="ランダムにコインを獲得します。")
async def earn(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        self.update_user(user_id)
        earned = random.randint(10, 50)
        self.data[user_id]["balance"] += earned
        save_data(self.data)
        await interaction.response.send_message(f"{interaction.user.mention} さん、{earned} コイン獲得しました♡")

@app_commands.command(name="shop", description="ショップのアイテムを表示します。")
async def shop(self, interaction: discord.Interaction):
# ショップアイテム例（アイテム名: 価格）
        shop_items = {
        "かわいいステッカー": 50,
        "キラキラペン": 100,
        "ふわふわクッション": 300
        }
        message = "【ショップアイテム】\n"
        for item, price in shop_items.items():
                message += f"- {item}: {price} コイン\n"
        await interaction.response.send_message(message)

@app_commands.command(name="buy", description="ショップからアイテムを購入します。")
@app_commands.describe(item="購入するアイテム名")
async def buy(self, interaction: discord.Interaction, item: str):
        shop_items = {
        "かわいいステッカー": 50,
        "キラキラペン": 100,
        "ふわふわクッション": 300
        }
        user_id = str(interaction.user.id)
        self.update_user(user_id)
        if item not in shop_items:
                await interaction.response.send_message("そのアイテムは見つかりませんでした…", ephemeral=True)
                return
        price = shop_items[item]
        if self.data[user_id]["balance"] < price:
                await interaction.response.send_message("コインが足りません！", ephemeral=True)
                return
        self.data[user_id]["balance"] -= price
        save_data(self.data)
        await interaction.response.send_message(f"{interaction.user.mention} さん、**{item}** を購入しました♡")

@app_commands.command(name="leaderboard", description="コインランキングを表示します。")
async def leaderboard(self, interaction: discord.Interaction):
# 所持コイン順で上位5名を表示
        sorted_users = sorted(self.data.items(), key=lambda x: x[1]["balance"], reverse=True)
        message = "【コインランキング】\n"
        for i, (user_id, info) in enumerate(sorted_users[:5], start=1):
                message += f"{i}位: <@{user_id}> - {info['balance']} コイン\n"
                await interaction.response.send_message(message)

async def setup(bot: commands.Bot):
        await bot.add_cog(EconomyCog(bot))