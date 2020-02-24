import os

import discord
from discord.ext import commands
from boto.s3.connection import S3Connection

from app.vending_machine import VendingMachine


class Trade(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = int(os.environ['COLOR'])

    @commands.command()
    async def shop(self, ctx) -> None:
        color = self.color
        coupons = VendingMachine().view_showcase()
        embed = discord.Embed(
            title='Vending Machine',
            description='To buy the coupons type: `;claim <id>`\nAvailable coupons',
            color=discord.Color(color)
        )

        for coupon in coupons:
            embed.add_field(name=f'{coupon[0]} - {coupon[1]}', value=f'{coupon[2]} ¢', inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def coin(self, ctx, member: discord.Member = None) -> None:
        user = member.id if member else ctx.author.id
        balance = VendingMachine().user_balance(user)
        color = self.color
        embed = discord.Embed(
            title='Balance:',
            description=f'{balance} ¢',
            color=discord.Color(color)
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def claim(self, ctx, coupon_id: str = None) -> None:
        if not coupon_id:
            await ctx.send('You forgot the `<id>` argument..')
            return

        coupon_verify = VendingMachine().buy_coupon(ctx.author.id, coupon_id)

        if coupon_verify[0] == "ok":
            await ctx.send(coupon_verify[1])
            await ctx.author.send(coupon_verify[2])
        else:
            await ctx.send(coupon_verify[1])


def setup(client):
    client.add_cog(Trade(client))
