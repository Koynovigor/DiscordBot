import discord
from discord.ext import commands
from random import choice
from responses import responses

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
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

client = commands.Bot(command_prefix = '/', intents = intents, application_command_guild_ids=[1236753402701025431])
@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.slash_command(name = "ответь", description = "Ответить на вопрос.")
async def ben(ctx, вопрос):
    await ctx.respond(f'— {вопрос}\n— {choice(responses)}')

@client.slash_command(name = "kick", description = "Кикнуть участника с сервера.")
@discord.default_permissions(administrator = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.send(f'Вы были исключены!')
    await member.kick(reason = reason)
    await ctx.respond(f'Пользователь {member.mention} был исключён!', ephemeral = True)

@client.slash_command(name = "ban", description = "Забанить участника на сервере.")
@discord.default_permissions(administrator = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.send(f'Вы были забанены!')
    await member.ban(reason = reason)
    await ctx.respond(f'Пользователь {member.mention} был забанен!', ephemeral = True)

@client.slash_command(name = "unban", description = "Разабанить участника на сервере.")
@discord.default_permissions(administrator = True)
async def unban(ctx, user_id: str):
    user = await client.fetch_user(user_id)
    try:
        await ctx.guild.unban(user)  # Попытка разбанить пользователя
        await ctx.respond(f'Пользователь {user.name} был разбанен.', ephemeral = True)
    except discord.NotFound:
        await ctx.respond(f'Пользователь {user_id} не найден.', ephemeral = True)
    except discord.HTTPException:
        await ctx.respond('Произошла ошибка при снятии бана.', ephemeral = True)

@client.slash_command(name = "mute", description = "Мьютит пользователя на определённое количесвто секунд")
@discord.default_permissions(administrator = True)
async def mute(ctx, user: discord.Member, duration: int):
    guild = ctx.guild
    mute_role = discord.utils.get(guild.roles, name = "Muted")

    # Проверка прав бота
    bot_member = guild.get_member(client.user.id)
    if not bot_member.guild_permissions.manage_roles:
        await ctx.respond("У меня нет прав на управление ролями.", hidden=True)
        return
    if not bot_member.guild_permissions.manage_channels:
        await ctx.respond("У меня нет прав на управление каналами.", hidden=True)
        return

    if not mute_role:
        mute_role = await guild.create_role(name = "Muted")
        for channel in guild.channels:
            await channel.set_permissions(mute_role, speak = False, send_messages = False, read_message_history = True, read_messages = True)

    await user.add_roles(mute_role)
    await ctx.respond(f'{user.mention} был замьючен на {duration} секунд.', ephemeral=True)
    await user.send(f'Вы были замьючены на {duration} секунд.')

    await asyncio.sleep(duration)
    await user.remove_roles(mute_role)
    await ctx.respond(f'{user.mention} был размьючен.', ephemeral=True)
    await user.send('Вы были размьючены.')

@client.slash_command(name = "clear", description = "Удалить предыдущие сообщения. Без аргумента удалится 2 сообщения")
@discord.default_permissions(administrator = True)
async def clear(ctx, number: int = 2):
    deleted = await ctx.channel.purge(limit = number)
    await ctx.respond(f"Удалено {len(deleted)} сообщение(ия).", ephemeral = True)

@client.slash_command(name = "ping", description = "Показывает пинг.")
async def ping(ctx):
    latency = round(client.latency * 1000)
    await ctx.respond(f'Pong!\nТвой пинг {latency} мс', ephemeral = True)

@client.message_command()
async def say(ctx, message):
    await ctx.respond(f'{ctx.author.name} said: {message.content}')

class BooleanConverter(commands.Converter):
  async def convert(self, ctx, argument):
    argument = argument.lower()
    if argument in ('yes', '1', 'true', 'enable', 'on'):
      return True
    if argument in ('no', '0', 'false', 'disable', 'off'):
      return False
    else:
      raise ValueError(f'Unknown value "{argument}" was passed.')


# @client.slash_command( name = "mode")
# async def toggle(ctx, mode: BooleanConverter):
#   await ctx.respond(f'The value is set to: {mode}')

@client.event
async def on_application_command_error(ctx, error):
  if isinstance(error, discord.ApplicationCommandInvokeError):
    await ctx.respond(str(error.original), ephemeral = True)

# from discord.ui import Button, View

# @client.slash_command(name="button", description="Display a button")
# async def button(ctx):
#     # Создание кнопки
#     button = Button(label="Click Me!", style=discord.ButtonStyle.green)
#     # Функция, вызываемая при нажатии на кнопку
#     async def button_callback(interaction):
#         await interaction.response.send_message("Thank you for clicking!", ephemeral=True)
#     # Подключение обработчика к кнопке
#     button.callback = button_callback
#     # Создание представления (View) и добавление кнопки в него
#     view = View()
#     view.add_item(button)
#     # Отправка сообщения с кнопкой
#     await ctx.respond("Hello! Here is your button:", view=view)



# intents = discord.Intents.default()
# intents.guilds = True
# intents.voice_states = True

# @client.slash_command(name = "private")
# async def private(guild):
#     # Создаем голосовой канал
#     new_channel = await guild.create_voice_channel(name = 'Создать [+]', category = 'Приватные комнаты')
#     global TARGET_CHANNEL_ID
#     TARGET_CHANNEL_ID = new_channel.id

# class MyView(discord.ui.View):
#     @discord.ui.button(
#             label = "Открыть", 
#             row = 0, 
#             style = discord.ButtonStyle.primary
#     )
#     async def open_button_callback(self, button, interaction):
#         # Открываем канал
#         await interaction.channel.set_permissions(
#             interaction.guild.default_role, 
#             connect = True,
#         )
#         await interaction.response.send_message("Канал открыт!", ephemeral = True)

#     @discord.ui.button(
#             label = "Закрыть", 
#             row = 0, 
#             style = discord.ButtonStyle.primary
#     )
#     async def close_button_callback(self, button, interaction):
#         # Закрываем канал
#         await interaction.channel.set_permissions(
#             interaction.guild.default_role, 
#             connect = False,
#         )
#         await interaction.response.send_message("Канал закрыт!", ephemeral = True)

# @client.event
# async def on_voice_state_update(member, before, after):
    
#     if after.channel and after.channel.id == TARGET_CHANNEL_ID:
#         guild = member.guild
#         category = after.channel.category
#         new_channel = await guild.create_voice_channel(
#             name = f'Приват от {member.name}',
#             category = category,
#             user_limit = 0
#         )
#         await member.move_to(new_channel)
#         await new_channel.send(f'{member.mention}, ваш личный канал создан!', view = MyView())

#     # Удаление канала, если он пустой
#     if before.channel and before.channel != after.channel:
#         if before.channel.id != TARGET_CHANNEL_ID and len(before.channel.members) == 0:
#             await before.channel.delete()

@client.slash_command(name = "moving", description = "Задаёт перемещение из канала в канал")
@discord.default_permissions(administrator = True)
async def moving(ctx, from_channel_id: str, to_channel_id: str):
    global from_channel, to_channel
    from_channel = int(from_channel_id)
    to_channel = int(to_channel_id)
    await ctx.respond(f'Автоматическое перемещенеи настроено из {from_channel_id} в {to_channel_id}', ephemeral = True)

@client.slash_command(name = "cler_moving", description = "Очищает перемещение")
@discord.default_permissions(administrator = True)
async def clear_moving(ctx):
    from_channel = None
    to_channel = None
    await ctx.respond('Перемещения очищены', ephemeral = True)

@client.event
async def on_voice_state_update(member, before, after):
    if from_channel is not None and to_channel is not None:
        if after.channel and after.channel.id == from_channel:
            # Если пользователь вошел в исходный голосовой канал, перемещаем его в целевой канал
            target_channel = member.guild.get_channel(to_channel)
            await member.move_to(target_channel)
            print(f"User {member.display_name} moved to {target_channel.name}")

@client.command()
@discord.default_permissions(administrator = True)
async def list_categories(ctx):
    categories = ctx.guild.categories
    if categories:
        category_list = "\n".join([f"{category.name} - {category.id}" for category in categories])
        await ctx.send(f"Категории на сервере:\n{category_list}")
    else:
        await ctx.send("На этом сервере нет категорий.")


from discord.ext import commands, tasks
from collections import defaultdict, deque
import time
import asyncio

# Настройки спама
MAX_MESSAGES = 5  # Максимальное количество сообщений
TIME_WINDOW = 10  # Временное окно в секундах
MUTE_DURATION = 60  # Длительность мьюта в секундах

# Хранение сообщений пользователей
user_messages = defaultdict(lambda: deque(maxlen=MAX_MESSAGES))

@client.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    current_time = time.time()
    user_messages[user_id].append(current_time)

    # Проверка на спам
    if len(user_messages[user_id]) == MAX_MESSAGES:
        if current_time - user_messages[user_id][0] < TIME_WINDOW:
            await mute_user(message.author, MUTE_DURATION)
            user_messages[user_id].clear()  # Очищаем сообщения пользователя после мьюта

    await client.process_commands(message)

async def mute_user(user, duration):
    guild = user.guild
    mute_role = discord.utils.get(guild.roles, name="Muted")

    if not mute_role:
        mute_role = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True, read_messages=True)

    await user.add_roles(mute_role)
    await user.send(f'Вы были замьючены на {duration} секунд за спам.')

    await asyncio.sleep(duration)
    await user.remove_roles(mute_role)
    await user.send('Вы были размьючены.')

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)