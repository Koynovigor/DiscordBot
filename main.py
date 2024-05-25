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

client = commands.Bot(command_prefix = '/', intents = discord.Intents.all(), application_command_guild_ids=[1236753402701025431])

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.slash_command(name = "ответь", description = "Ответить на вопрос.")
async def ben(ctx, вопрос):
    await ctx.respond(f'— {вопрос}\n— {choice(responses)}')

@client.slash_command(name = "kick", description = "Кикнуть участника с сервера.")
@discord.default_permissions(administrator = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.respond(f'Пользователь {member.mention} был исключён!', ephemeral = True)

@client.slash_command(name = "ban", description = "Забанить участника на сервере.")
@discord.default_permissions(administrator = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.respond(f'Пользователь {member.mention} был забанен!', ephemeral = True)

@client.user_command()
async def ban(ctx, user):
    await user.ban()
    await ctx.respond(f'Пользователь {user.mention} был забанен!', ephemeral = True)

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

@client.slash_command( name = "mode")
async def toggle(ctx, mode: BooleanConverter):
  await ctx.respond(f'The value is set to: {mode}')

@client.event
async def on_application_command_error(ctx, error):
  if isinstance(error, discord.ApplicationCommandInvokeError):
    await ctx.respond(str(error.original))

from discord.ui import Button, View

@client.slash_command(name="button", description="Display a button")
async def button(ctx):
    # Создание кнопки
    button = Button(label="Click Me!", style=discord.ButtonStyle.green)
    # Функция, вызываемая при нажатии на кнопку
    async def button_callback(interaction):
        await interaction.response.send_message("Thank you for clicking!", ephemeral=True)
    # Подключение обработчика к кнопке
    button.callback = button_callback
    # Создание представления (View) и добавление кнопки в него
    view = View()
    view.add_item(button)
    # Отправка сообщения с кнопкой
    await ctx.respond("Hello! Here is your button:", view=view)



intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

@client.event
async def on_guild_join(guild):
    category = await guild.create_category('Приватные комнаты')  # Можно указать категорию, если необходимо

    # Создаем голосовой канал
    new_channel = await guild.create_voice_channel(name = 'Создать [+]', category = category)
    global TARGET_CHANNEL_ID
    TARGET_CHANNEL_ID = new_channel.id

class MyView(discord.ui.View):
    @discord.ui.button(
            label = "Открыть", 
            row = 0, 
            style = discord.ButtonStyle.primary
    )
    async def open_button_callback(self, button, interaction):
        # Открываем канал
        await interaction.channel.set_permissions(
            interaction.guild.default_role, 
            connect = True,
        )
        await interaction.response.send_message("Канал открыт!", ephemeral = True)

    @discord.ui.button(
            label = "Закрыть", 
            row = 0, 
            style = discord.ButtonStyle.primary
    )
    async def close_button_callback(self, button, interaction):
        # Закрываем канал
        await interaction.channel.set_permissions(
            interaction.guild.default_role, 
            connect = False,
        )
        await interaction.response.send_message("Канал закрыт!", ephemeral = True)

@client.event
async def on_voice_state_update(member, before, after):
    
    if after.channel and after.channel.id == TARGET_CHANNEL_ID:
        guild = member.guild
        category = after.channel.category
        new_channel = await guild.create_voice_channel(
            name = f'Приват от {member.name}',
            category = category,
            user_limit = 0
        )
        await member.move_to(new_channel)
        await new_channel.send(f'{member.mention}, ваш личный канал создан!', view = MyView())

    # Удаление канала, если он пустой
    if before.channel and before.channel != after.channel:
        if before.channel.id != TARGET_CHANNEL_ID and len(before.channel.members) == 0:
            await before.channel.delete()

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)