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