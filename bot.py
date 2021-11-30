from collections import deque
from basic import Basic
import discord
from discord.ext import commands
from dotenv import load_dotenv
from music import Music
from basic import Basic 
import os

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.')
bot.add_cog(Music(bot))
bot.add_cog(Basic(bot))

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(".help | Early Alpha v0.3"))

bot.run(TOKEN)
