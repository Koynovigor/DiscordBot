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

"""
@client.slash_command(name="hello", description="Greet the user")
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.author.name}!")

@client.message_command(name="Reverse Message")
async def reverse(ctx, message: discord.Message):
    await ctx.respond(message.content[::-1])

@client.user_command(name="Get ID")
async def get_id(ctx, user: discord.User):
    await ctx.respond(f"The ID of {user.name} is {user.id}")

"""


"""
# Функция для загрузки расширения
@client.slash_command(name = "load", description = "Load a cogs")
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

# Функция для перезагрузки расширения
@client.command()
@commands.has_permissions(administrator = True) # Убедитесь, что команды могут использовать только администраторы
async def reload(ctx, extension):
    try:
        await client.unload_extension(f'cogs.{extension}')
        await client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Расширение {extension} перезагружено.')
    except Exception as e:
        await ctx.send(f'Произошла ошибка при перезагрузке {extension}: {str(e)}')

# Загрузка всех расширений из папки cogs при запуске бота
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        extension = filename[:-3]
        try:
            client.load_extension(f'cogs.{extension}')
            print(f'Загружено расширение: {extension}')
        except Exception as e:
            print(f'Не удалось загрузить {extension}: {str(e)}')
"""

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

# class MusicPlayer(View):
#     def __init__(self):
#         super().__init__(timeout = None)  # Timeout = None чтобы кнопки оставались активными

#     @discord.ui.button(label = "Play", style = discord.ButtonStyle.green)
#     async def play(self, interaction: discord.Interaction, button: discord.ui.Button):
#         # Здесь код для воспроизведения музыки
#         await interaction.response.send_message("Playing music...", ephemeral = True)

#     @discord.ui.button(label = "Pause", style=discord.ButtonStyle.red)
#     async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
#         # Здесь код для паузы музыки
#         await interaction.response.send_message("Music paused.", ephemeral = True)

#     @discord.ui.button(label = "Stop", style = discord.ButtonStyle.grey)
#     async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
#         # Здесь код для остановки музыки
#         await interaction.response.send_message("Music stopped.", ephemeral = True)

# @client.slash_command(name = "music", description = "Controls for music player.")
# async def music(ctx):
#     await ctx.respond("Here are your music controls:", view = MusicPlayer())


# @client.slash_command(name = "join")
# async def join(ctx):
#     channel = ctx.author.voice.channel
#     await channel.connect()

# @client.slash_command(name = "play")
# async def play(ctx, url):
#     voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     if not voice_client:
#         await ctx.send("Бот не подключен к голосовому каналу.")
#         return
#     ffmpeg_audio_source = ffmpeg.fftools.ff
#     voice_client.play(ffmpeg_audio_source)

# @client.slash_command(name = "leave")
# async def leave(ctx):
#     voice_client = discord.utils.get(client.voice_clients, guild = ctx.guild)
#     if voice_client:
#         await voice_client.disconnect()

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)