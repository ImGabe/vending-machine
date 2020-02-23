import os

from boto.s3.connection import S3Connection

from discord.ext import commands


client = commands.Bot(command_prefix=os.environ['TOKEN'])
