import discord
from discord.ext import commands
from discord import app_commands
from func.log import get_log
from pydantic import BaseModel
import func.status as status
import func.presence as presence

class Channels(BaseModel):
    id:int
    name: str

class PresenceCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.log = get_log(self.__class__.__name__)
    @commands.Cog.listener()
    async def on_ready(self):
        self.log.info(f"{self.__class__.__name__}が読み込まれました！")
    @commands.Cog.listener()
    async def on_presence_update(self, before:discord.Member, new:discord.Member):
        channel = presence.get_channel(new.id)
        if channel:
            match new.status:
                case discord.Status.online:
                    st = "online"
                case discord.Status.idle:
                    st = "online"
                case discord.Status.dnd:
                    st = "online"
                case discord.Status.offline:
                    st = "offline"
            if st == status.get_status(new.id):
                return
            channel = self.bot.get_channel(channel.id)
            embed: discord.Embed = None

            if st == "online":
                embed = discord.Embed(
                    title=f"<:online:1462372462711799913> オンラインになりました",
                    description=f"{channel.name}がオンラインになりました。"
                )
                if new.avatar.url:
                    embed.set_thumbnail(url=new.avatar.url)
            if st == "offline":
                embed = discord.Embed(
                    title=f"<:offline:1462372516071870609> オフラインになりました",
                    description=f"{channel.name}がオフラインになりました。"
                )
                if new.avatar.url:
                    embed.set_thumbnail(url=new.avatar.url)
            if embed:
                webhook: discord.Webhook = None
                webhooks: list[discord.Webhook] = await channel.webhooks()
                #print(webhooks)
                if len(webhooks) == 0:
                    webhook = await channel.create_webhook(name=f"Bot Notice + Hook")
                else:
                    for i in webhooks:
                        if i.type != discord.WebhookType.channel_follower:
                            webhook = i
                    if webhook == None:
                        webhook = await channel.create_webhook(name=f"Bot Notice + Hook")
                await webhook.send(
                    username="BOT Status",
                    avatar_url=self.bot.user.avatar.url,
                    embed=embed
                )
            status.set_status(new.id, st)
    @app_commands.command(name="add_bot")
    async def add(self, interaction:discord.Interaction, bot:discord.Member, channel:str):
        if interaction.user.guild_permissions.administrator:
            _id = int(channel)
            presence.set_channel(bot.id, Channels(id=_id, name=bot.name))
            await interaction.response.send_message("ok")

async def setup(bot):
    await bot.add_cog(PresenceCog(bot))
