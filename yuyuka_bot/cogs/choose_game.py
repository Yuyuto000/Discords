import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
import random

class ChooseGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ゲームの開始
    @app_commands.command(name="choose_game",descripition="宝探ししよ？❤")
    async def choose_game(self, ctx: discord.ApplicationContext):
        await ctx.send("選択肢が3つ！自分を信じて選んでね！💫", view=self.ChooseView())

    # 選択肢のボタンビュー
    class ChooseView(View):
        def __init__(self):
            super().__init__(timeout=30)

        @discord.ui.button(label="🌟星の力", style=discord.ButtonStyle.primary)
        async def star_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            result = random.choice(["✨大成功！✨", "🌌何も得られなかった…", "🌠素敵な運命が待っている！"])
            await interaction.response.send_message(f"あなたの選択は「星の力」！結果は... {result}", ephemeral=True)

        @discord.ui.button(label="💎宝石の力", style=discord.ButtonStyle.primary)
        async def gem_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            result = random.choice(["💎大当たり！", "💍ただの石でした", "💫幸運が訪れるかも！"])
            await interaction.response.send_message(f"あなたの選択は「宝石の力」！結果は... {result}", ephemeral=True)

        @discord.ui.button(label="🍀運命の力", style=discord.ButtonStyle.primary)
        async def fate_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            result = random.choice(["🍀素晴らしい運命が訪れた！", "🎲ちょっとした冒険が始まる", "🍃残念、次のチャンスだ！"])
            await interaction.response.send_message(f"あなたの選択は「運命の力」！結果は... {result}", ephemeral=True)

# スラッシュコマンドをセットアップ
async def setup(bot: commands.Bot):
    await bot.add_cog(ChooseGame(bot))
    await bot.tree.sync()
