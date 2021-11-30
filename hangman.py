import discord
from discord.ext import commands
from discord.errors import Forbidden
import re
import random

async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information abot missing permissions
    """
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.player = None
        self.word = None
        self.guessed_word = None

    @commands.command(name="hang-create", help="Creates a new Hangman Game for a specific user")
    async def hangman_create(self, ctx):
        self.player = ctx.message.author
        await ctx.send("Wait a bit.. it's being implemented")

    
