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


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        await channel.send(f'Hello and welcome on {member.guild.name} {member.name.mention}! :smile:')

    @commands.command(name='duck', help="Gives you a duckduckgo link for the given search values! Usage: .duck <searchValue 1>-<searchValue 2> ...")
    async def duck_link(self, ctx, *, message):
        if len(message) < 1:
        	await ctx.send('Invalid arguments! Usage: .duck <searchValue 1> <searchValue 2> ...')
        	return
	
        parts = ""
        for part in message:
            parts += part
	
        parts = re.sub(r"\s", '_', parts)

        link = 'https://www.duckduckgo.com/' + parts
        emb = discord.Embed(title=':mag: DuckDuckGo', color=discord.Color.orange())
        emb.add_field(name='Information', value=f"Requested by {ctx.message.author.mention}", inline=False)
        emb.add_field(name='Link', value=f'{link}', inline=False)
        await send_embed(ctx, emb)

    @commands.command(name='flip', help="Toss a coin")
    async def coin_flip(self, ctx):
        toss = random.randint(0, 1)
        emb = None
        if toss == 1:
            emb = discord.Embed(title=f":coin: You got **TAIL**", color=discord.Color.blue())
        else:
            emb = discord.Embed(title=f":coin: You got **HEAD**", color=discord.Color.blue())
        await send_embed(ctx, emb)
