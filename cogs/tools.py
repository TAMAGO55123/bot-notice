import discord
from discord.ext import commands
from discord import app_commands
from func.log import get_log

class ToolsCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.log = get_log(self.__class__.__name__)
    @commands.Cog.listener()
    async def on_ready(self):
        self.log.info(f"{self.__class__.__name__}が読み込まれました！")

    @app_commands.command(name="cid")
    async def cid(self, interaction:discord.Interaction, channel: discord.TextChannel = None):
        ch = channel if channel else interaction.channel
        await ch.send(ch.id)

async def setup(bot):
    await bot.add_cog(ToolsCog(bot))
