import discord
from discord.ext import commands
from random import choice
from responses import responses

class Ben(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Событие, которое активируется, когда бот полностью готов и работает
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ben is ready')

    @commands.command(aliases = ['ответь'])
    async def ben(self, ctx, *, question):
        await ctx.reply(choice(responses))

async def setup(client):
    await client.add_cog(Ben(client))