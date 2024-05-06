import discord
import os
from discord.ext import commands
import asyncio

from token_1 import DISCORD_TOKEN
# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
"""
logging.debug("Это сообщение отладки")
logging.info("Информационное сообщение")
logging.warning("Предупреждение")
logging.error("Ошибка")
logging.critical("Критическая ошибка")
"""

client = commands.Bot(command_prefix = '/', intents = discord.Intents.all())

# Функция для загрузки расширения
@client.command()
@commands.has_permissions(administrator = True)  # Убедитесь, что команды могут использовать только администраторы
async def load(ctx, extension):
    try:
        await client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Расширение {extension} загружено.')
    except Exception as e:
        await ctx.send(f'Произошла ошибка при загрузке {extension}: {str(e)}')

# Функция для выгрузки расширения
@client.command()
@commands.has_permissions(administrator = True) # Убедитесь, что команды могут использовать только администраторы
async def unload(ctx, extension):
    try:
        await client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Расширение {extension} выгружено.')
    except Exception as e:
        await ctx.send(f'Произошла ошибка при выгрузке {extension}: {str(e)}')


# Загрузка всех расширений из папки cogs при запуске бота
async def load_all_extensions():
    for filename in os.listdir('.\cogs'):
        if filename.endswith('.py'):
            extension = filename[:-3]
            try:
                await client.load_extension(f'cogs.{extension}')
                print(f'Загружено расширение: {extension}')
            except Exception as e:
                print(f'Не удалось загрузить {extension}: {str(e)}')

if __name__ == "__main__":
    asyncio.run(load_all_extensions())
    client.run(DISCORD_TOKEN)