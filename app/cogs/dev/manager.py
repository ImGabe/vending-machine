import discord
from discord.ext import commands

from app.data.models import CouponModel, TxModel
from app import config


class Manager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.manager = config['CLIENT']['MANAGER_ID']

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def insert_coupon(self, ctx, description: str, code: str, cost: int) -> None:
        if ctx.author.id != self.manager:
            return

        CouponModel().insert_model(description, code, cost)
        await ctx.send('Ok!')

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

        TxModel().insert_model(member.id, value)
        await ctx.send('Ok!')


def setup(client):
    client.add_cog(Manager(client))
