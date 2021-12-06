from collections import deque
from basic import Basic
import discord
from discord.ext import commands
from dotenv import load_dotenv
from hangman import Hangman
from music import Music
from basic import Basic 
import os

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)
bot.add_cog(Music(bot))
bot.add_cog(Basic(bot))
bot.add_cog(Hangman(bot))

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(".help | Early Alpha v0.4"))

bot.run(TOKEN)
