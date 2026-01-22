import discord
from discord.ext import commands
from discord import app_commands
from func.log import get_log
from pydantic import BaseModel

class Channels(BaseModel):
    channel: discord.TextChannel
    name: str
    model_config = {
        "arbitrary_types_allowed": True
    }

class KuronekoCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.log = get_log(self.__class__.__name__)
    @commands.Cog.listener()
    async def on_ready(self):
        self.log.info(f"{self.__class__.__name__}が読み込まれました！")
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        def create_channel_ob(channel_id: int, name: str):
            return Channels(
                channel=message.guild.get_channel(channel_id),
                name=name
            )
        # print(message)
        # print(message.content)
        if message.channel.id == 1462348330934866021:
            channels: list[Channels] = []
            if "VOICEVOX" in message.content or "全読み上げ" in message.content:
                channels.append(create_channel_ob(1462398980116713525,"VOICEVOX読み上げbot"))
            if "VOICEROID" in message.content or "全読み上げ" in message.content:
                channels.append(create_channel_ob(1462399018163245120, "VOICEROID読み上げbot"))
            if len(channels) != 0:
                for channel in channels:
                    webhook: discord.Webhook = None
                    webhooks: list[Channels] = await channel.channel.webhooks()
                    if len(webhooks) == 0:
                        webhook = await channel.channel.create_webhook(name=f"Bot Notice + Hook")
                    else:
                        for i in webhooks:
                            if i.type != discord.WebhookType.channel_follower:
                                webhook = i
                        if webhook == None:
                            webhook = await channel.create_webhook(name=f"Bot Notice + Hook")
                    await webhook.send(
                        username=f"KuronekoServer | {channel.name}",
                        avatar_url="https://cdn.discordapp.com/attachments/1462355119894171941/1462355134880288863/image.png",
                        allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False),
                        content=message.clean_content
                    )
                
        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(KuronekoCog(bot))
