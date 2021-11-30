import discord
from discord.ext import commands
from discord.errors import Forbidden
import re

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
    	await ctx.send(f"{ctx.message.author.mention} Here is your requested link: " + link)
