import discord
from discord.ext import commands
from token_1 import DISCORD_TOKEN
import logging
from random import choice
from responses import responses

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
"""
logging.debug("Это сообщение отладки")
logging.info("Информационное сообщение")
logging.warning("Предупреждение")
logging.error("Ошибка")
logging.critical("Критическая ошибка")
"""

client = commands.Bot(command_prefix = '.', intents = discord.Intents.all())

@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')

@client.command(aliases = ['ответь'])
async def ben(ctx, *, question):
    await ctx.reply(choice(responses))

@client.command()
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.channel.purge(limit = 1)
    await ctx.send(f'Пользователь {member.mention} был исключён!')

@client.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.channel.purge(limit = 1)
    await ctx.send(f'Пользователь {member.mention} был забанен!')

@client.command()
async def clear(ctx, amout = 2):
    await ctx.channel.purge(limit = amout)

@client.command()
async def unban(ctx, user_id: int):
    user = await client.fetch_user(user_id)
    try:
        await ctx.guild.unban(user)  # Попытка разбанить пользователя
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'Пользователь {user.name} был разбанен.')
    except discord.NotFound:
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'Пользователь {user_id} не найден.')
    except discord.HTTPException:
        await ctx.channel.purge(limit = 1)
        await ctx.send('Произошла ошибка при снятии бана.')



client.run(DISCORD_TOKEN)