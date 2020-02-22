from pathlib import Path
import configparser
import json

import discord

from app import client, config


@client.event
async def on_ready():
    await client.change_presence(
        status=config['CLIENT']['STATUS'],
        activity=discord.Game(config['CLIENT']['ACTIVITY']))

    print('Up and running!')


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
    load_extensions(config['DEFAULT']['COG_DIR'])
    client.run(config['CLIENT']['TOKEN'])
