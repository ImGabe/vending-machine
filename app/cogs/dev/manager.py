import discord
from discord.ext import commands

from app.data.models import CouponModel, TxModel
from app import config


class Manager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.manager = int(config['CLIENT']['MANAGER_ID'])

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def insert_coupon(self, ctx, description: str, code: str, cost: int) -> None:
        if ctx.author.id != self.manager:
            return

        await ctx.send(CouponModel().insert_model(description, code, cost))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reward(self, ctx,  member: discord.Member = None, value: int = None) -> None:
        if ctx.author.id != self.manager:
            return

        if not member:
            await ctx.send('You forgot the `<member>` argument.')
            return

        if not isinstance(member, discord.Member):
            await ctx.send('Couldn\'t find the user.')
            return

        if not value:
            await ctx.send('You forgot the `<value>` argument.')
            return

        await ctx.send(TxModel().insert_model(member.id, value)[1])


def setup(client):
    client.add_cog(Manager(client))
