from collections import deque
import os
import re
import asyncio
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from yt_utils.YTDLSource import YTDLSource
from collections import deque

load_dotenv()

queue = deque()
volume = 50

TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
	print(f'{client.user.name} is connected to Discord!')

@client.event
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(f'WAAAAAAAAAAAAAAAAAAAAAAAAASUUUUUP {member.name.mention}!')

@client.command(name='duck', help="Gives you a duckduckgo link for the given search values! Usage: .duck <searchValue 1>-<searchValue 2> ...")
async def duck_link(ctx, *, message):
	if len(message) < 1:
		await ctx.send('Invalid arguments! Usage: .duck <searchValue 1> <searchValue 2> ...')
		return
	
	parts = ""
	for part in message:
		parts += part
	
	parts = re.sub(r"\s", '_', parts)
	

	link = 'https://www.duckduckgo.com/' + parts
	await ctx.send(f"{ctx.message.author.mention} Here is your requested link: " + link)

@client.command(name='quit', help="If you think i can be quitted, you're wrong!")
async def quit_bot(ctx):
	

	if "mexam" in ctx.message.author.name:
		await ctx.send(f"I shall not be quitted! Ach ja, und {ctx.message.author.mention} ist cool ;)")
	else:
		await ctx.send(f"I shall not be quitted! Ach ja, und {ctx.message.author.mention} ist ein Noob ;)")

@client.command(name='leave', help="Leaves the voice channel")
async def exit_voice(ctx):
	global queue
	try:
		await ctx.voice_client.disconnect()
		await ctx.send("Sucessfully left the voice channel")
		if len(queue) > 0:
			queue = []
	except Exception as e:
		print(e)
		await ctx.send(f"ERROR: {ctx.message.author.mention} You stupid? I'm not in a voice channel!")
		
@client.command(name='skip', help="Skips the current song")
async def skip_music(ctx):
	try:
		await ctx.send("Aight, gonna skip this!")
		ctx.voice_client.stop()
	except:
		await ctx.send("You're not in a voice channel!")

@client.command(name='pause', help="pauses the music")
async def pause_music(ctx):
	try:
		ctx.voice_client.pause()
		await ctx.send("Pausing music")
	except:
		await ctx.send("You're not in a voice channel")

@client.command(name='resume', help="Resumes playing music")
async def resume_music(ctx):
	try:
		ctx.voice_client.resume()
		await ctx.send("Resuming music")
	except:
		await ctx.send("You're not in a voice channel!")

@client.command(name="volume", aliases=['v', 'vol'], help="Sets the volume for MEXAM (values from 0-100) usage: .volume (shows current volume) / .volume <number> (sets volume to <number>%)")
async def volume_set(ctx, value=-1):
	global volume
	if value == -1:
		await ctx.send(f"Volume is currently at {volume}%")
		return
	try:
		volume = value
		ctx.voice_client.source.volume = int(value) / 100
		await ctx.send(f"Volume set to {volume}%")
	except:
		await ctx.send("You're not in a voice channel")

@client.command(name='yt', help="Play Songs from Youtube!")
async def play(ctx, *, input):
	global queue
	try:
		channel = ctx.author.voice.channel
		voice_channel = discord.utils.get(client.voice_clients, guild=ctx.message.guild)
		if voice_channel is None:
			voice_channel = await channel.connect()
		
		if "youtube.com" in input:
			song = await YTDLSource.from_url(input, loop=client.loop)
			queue.append((ctx.message.guild, song))
			if not voice_channel.is_playing() and not voice_channel.is_paused():
				await play_queue(ctx, voice_channel)
			else:
				await ctx.send(f"Queued {song[0].title}")
		else:
			song = await YTDLSource.from_text(input, loop=client.loop)
			queue.append((ctx.message.guild, song))
			if not voice_channel.is_playing() and not voice_channel.is_paused():
				await play_queue(ctx, voice_channel)
			else:
				await ctx.send(f"Queued {song[0].title}")
		
	except Exception as e:
		print(e)
		await ctx.send(f"You're not in a voice channel {ctx.message.author.mention} ")	


@client.command(name='queue', help="Shows the current youtube queue")
async def queue_show(ctx):
	global queue
	songs = ""
	count = 0
	for i, j in queue:
		if ctx.message.guild == i:
			count += 1
			songs += str(count) + ". " + j[0].title + "\n"
	if count == 0:
		await ctx.send("No songs in queue!")
	else:
		await ctx.send(songs)

#TODO: implement clear_queue

async def play_queue(ctx, voice_channel):
	global queue
	while len(queue) > 0:
		item = queue.popleft()
		for i in range(len(queue), 0, -1):
			if queue[i][0] == ctx.message.guild:
				item = queue[i]
				queue.remove(item)
		if item[0] == ctx.message.guild:
			voice_channel.play(item[1][0])
			ctx.voice_client.source.volume = volume / 100
			await ctx.send(f'Now playing: {item[1][0].title}')
			while voice_channel.is_playing() or voice_channel.is_paused():
				await asyncio.sleep(1)
			os.system("rm -r " + item[1][1])
		else:
			pass
	await voice_channel.disconnect()
	await ctx.send("That's everything you added. Gonna stop now!")
	

client.run(TOKEN)
