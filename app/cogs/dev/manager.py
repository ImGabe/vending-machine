import os

import discord
from discord.ext import commands
from boto.s3.connection import S3Connection

from app.data.models import CouponModel, TxModel


class Manager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.manager = int(os.environ['MANAGER_ID'])
        self.helper = int(os.environ['HELPER_ID']) or None
        self.staff = [self.manager, self.helper]

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def insert_coupon(self, ctx, description: str, code: str, cost: int) -> None:
        if not ctx.author.id in self.staff:
            return

        await ctx.send(CouponModel().insert_model(description, code, cost))
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx) -> None:
        if ctx.author.id != self.manager:
            return

        TxModel().reset()
        CouponModel().reset()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reward(self, ctx,  member: discord.Member = None, value: int = None) -> None:
        if not ctx.author.id in self.staff:
            return

        if not member:
            await ctx.send('You forgot the `<member>` argument.')
            return

        if not value:
            await ctx.send('You forgot the `<value>` argument.')
            return

        await ctx.send(TxModel().insert_model(member.id, value)[1])


def setup(client):
    client.add_cog(Manager(client))
