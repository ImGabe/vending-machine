import configparser
import json

from discord.ext import commands


config = configparser.ConfigParser()
config.read('config.ini')

client = commands.Bot(command_prefix=config['CLIENT']['PREFIX'])
