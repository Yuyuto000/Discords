import discord
from discord import app_commands
from discord.ext import commands
import random

class JankenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="janken", description="じゃんけんやろ❤")
    async def janken(self, interaction: discord.Interaction):
        # じゃんけんの手を定義
        choices = ["グー", "チョキ", "パー"]
        
        # 初期メッセージ送信
        embed = discord.Embed(
            title="じゃんけん！",
            description="グー、チョキ、パーの中から選んでね❤",
            color=discord.Color.blue()
        )
        embed.set_footer(text="対応するボタンを押して手を選んで！")
        await interaction.response.send_message(embed=embed, view=JankenView(choices))

class JankenView(discord.ui.View):
    def __init__(self, choices):
        super().__init__(timeout=None)  # タイムアウトを無効化
        self.choices = choices

    @discord.ui.button(label="✊", style=discord.ButtonStyle.primary)
    async def rock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_interaction(interaction, "グー")

    @discord.ui.button(label="✌", style=discord.ButtonStyle.success)
    async def scissors_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_interaction(interaction, "チョキ")

    @discord.ui.button(label="✋", style=discord.ButtonStyle.danger)
    async def paper_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_interaction(interaction, "パー")

    async def handle_interaction(self, interaction: discord.Interaction, user_choice: str):
        bot_choice = random.choice(self.choices)
        result = self.determine_result(user_choice, bot_choice)

        # 結果の埋め込みメッセージ
        embed = discord.Embed(
            title="じゃんけんの結果！",
            color=discord.Color.green() if result == "勝ち" else discord.Color.red() if result == "負け" else discord.Color.yellow()
        )
        embed.add_field(name="あなたの手", value=user_choice, inline=True)
        embed.add_field(name="Botの手", value=bot_choice, inline=True)
        embed.add_field(name="結果", value=result, inline=False)

        # あいこの場合は続けるためにボタンを維持
        if result == "あいこ":
            embed.set_footer(text="あいこだよ！もう一回！")
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            embed.set_footer(text="おわり！また遊んでね❤")
            self.stop()  # ボタンを無効化
            await interaction.response.edit_message(embed=embed, view=None)

    def determine_result(self, user_choice, bot_choice):
        if user_choice == bot_choice:
            return "あいこ"
        elif (user_choice == "グー" and bot_choice == "チョキ") or \
             (user_choice == "チョキ" and bot_choice == "パー") or \
             (user_choice == "パー" and bot_choice == "グー"):
            return "勝ち"
        else:
            return "負け"

async def setup(bot):
    await bot.add_cog(JankenCog(bot))
    await bot.tree.sync()
