import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Событие, которое активируется, когда бот полностью готов и работает
    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation is ready')
    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx, member : discord.Member, *, reason = None):
        await member.kick(reason = reason)
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'Пользователь {member.mention} был исключён!')

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        await member.ban(reason = reason)
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'Пользователь {member.mention} был забанен!')

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amout = 2):
        await ctx.channel.purge(limit = amout)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unban(self, ctx, user_id: int):
        user = await self.client.fetch_user(user_id)
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

def setup(client):
    client.add_cog(Moderation(client))