from func.log import get_log, stream_handler
import asyncio
import discord
from discord import app_commands
from discord.ext import commands, tasks
from os import getenv, listdir
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="gn_", intents=intents)

TOKEN = getenv("TOKEN")

main_log = get_log("Main")

async def main(bot:commands.Bot):
    log = main_log
    try:
        @bot.event
        async def on_ready():
            log.info(f"{bot.user}としてログインしました^o^")
        @bot.event
        async def setup_hook():
            try:
                for cog in listdir("cogs"):
                    if cog.endswith(".py"):
                        await bot.load_extension(f"cogs.{cog[:-3]}")
                synced = await bot.tree.sync()
                log.info(f"{len(synced)}個のコマンドを同期しました。")
            except Exception as e:
                log.error(f"コマンドの同期中にエラーが発生しました。")
                
        class SendEmbedModal(discord.ui.Modal):
            def __init__(self, channel:discord.TextChannel, message:str):
                super().__init__(
                    title="フォーム",
                    timeout=None,
                )
    
                self.messages = discord.ui.TextInput(
                    label="Color Code",
                    style=discord.TextStyle.short,
                    max_length=6,
                    required=False,
                )
                self.add_item(self.messages)
    
                self.channel = channel
                self.message = message
    
            async def on_submit(self, interaction:discord.Interaction):
                if self.messages.value:
                    a = int(f"0x{self.messages.value}", 16)
                else:
                    a = None
                await self.channel.send(embed=discord.Embed(description=self.message, color=a))
                await interaction.response.send_message("sended.",ephemeral=True)
    
        @bot.tree.context_menu(name="メッセージを再送信")
        async def message_re_send(interaction:discord.Interaction, message:discord.Message):
            if interaction.user.guild_permissions.administrator:
                await message.channel.send(content=message.content, embeds=message.embeds)
                await interaction.response.send_message(content="sended.",ephemeral=True)
            else:
                await interaction.response.send_message(content="このアプリは、管理者のみ実行可能です。", ephemeral=True)
    
        @bot.tree.context_menu(name="メッセージを埋め込みに変換")
        async def message_send_embed(interaction:discord.Interaction, message:discord.Message):
            if interaction.user.guild_permissions.administrator:
                modal = SendEmbedModal(channel=message.channel, message=message.content)
                await interaction.response.send_modal(modal)
            else:
                await interaction.response.send_message(content="このアプリは、管理者のみ実行可能です。", ephemeral=True)
    
    @bot.tree.context_menu(name="埋め込みをメッセージに変換")
    async def embed_send_message(interaction:discord.Interaction, message:discord.Message):
        if interaction.user.guild_permissions.administrator:
            a = ""
            for i in message.embeds:
                a = a + i.description
            await message.channel.send(content=a)
            await interaction.response.send_message("sended.", ephemeral=True)
        else:
            await interaction.response.send_message(content="このアプリは、管理者のみ実行可能です。", ephemeral=True)

        await bot.start(TOKEN)
    except Exception as e:
        log.error(f"BOTの起動中にエラーが発生しました\n{e}")
        
try:
    discord.utils.setup_logging(handler=stream_handler)
    asyncio.run(main(bot=bot))
except KeyboardInterrupt:
    asyncio.run(bot.close())
except Exception as e:
    print(f'エラーが発生しました: {e}')