from pathlib import Path
import os

import discord
from boto.s3.connection import S3Connection

from app import client
from app.cogs.dev.manager import Manager


@client.event
async def on_ready():
    await client.change_presence(
        status=os.environ['STATUS'],
        activity=discord.Game(os.environ['ACTIVITY']))

    print('Up and running!')


@client.event
async def on_message(message):
    if message.id == 159985870458322944:
        [command, _user, value] = message.content.split(' ')

        if command == ';reward':
            await Manager(client).reward(message.mentions[0], value)


def load_extensions(cogs: str) -> None:
    '''
    Loads all extensions recursively.\n
    Params:
        cogs: str
        Relative path to cogs dir.
    '''

    for extension in Path(cogs).rglob('*.py'):
        extension = '.'.join(extension.parts)[:-3]

        try:
            client.load_extension(extension)
            print(f'{extension} has been loaded.')
        except Exception as e:
            print(f'{extension} could not be loaded: {e}')


if __name__ == '__main__':
    load_extensions(os.environ['COG_DIR'])
    client.run(os.environ['TOKEN'])
