import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
import random

class PopGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ぽっぷゲームの開始
    @app_commands.command(name="pop_game",descripition="ぽっぷゲームを開催！")
    async def pop_game(self, ctx: discord.ApplicationContext):
        # ぽっぷゲームのメッセージ
        await ctx.send("準備はいい？ ぽっぷ！ボタンを押してね！💥", view=self.PopGameView())

    # ゲームのインタラクション用ビュー
    class PopGameView(View):
        def __init__(self):
            super().__init__(timeout=30)

        @discord.ui.button(label="ぽっぷ！", style=discord.ButtonStyle.primary)
        async def pop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            # ぽっぷボタンを押したときの動作
            result = random.choice(["🎉", "💥", "✨", "🎈"])
            await interaction.response.send_message(f"ぽっぷ！結果は... {result}", ephemeral=True)

        @discord.ui.button(label="リセット", style=discord.ButtonStyle.danger)
        async def reset_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("ゲームをリセットしました！もう一度試してみてね！🌸", ephemeral=True)
            self.stop()

# スラッシュコマンドをセットアップ
async def setup(bot: commands.Bot):
    await bot.add_cog(PopGame(bot))
    await bot.tree.sync()
