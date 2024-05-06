import discord
from discord.ext import commands

class Ping(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    # Событие, которое активируется, когда бот полностью готов и работает
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ping is ready')

    # Commands
    @commands.command()
    async def ping(self, ctx):
        latency = round(self.client.latency * 1000)
        await ctx.send(f'Pong! {latency} ms')


def setup(client):
    client.add_cog(Ping(client))
