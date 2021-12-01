import discord
from discord.ext import commands
from discord.errors import Forbidden
from discord import FFmpegPCMAudio
from collections import deque
import os
import asyncio
from yt_utils.YTDLSource import YTDLSource


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

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.queue = deque()
        self.volume = []
        self.skipping = [":cry: Aight, gonna skip this!", ":face_exhaling: DJ Skip at work!", ":angry: And skipping again...", ":rage: Dude, srsly?? ... Ok, skipped"]
        self.i = 0

    async def play_queue(self, ctx, voice_channel):
        while len(self.queue) > 0:
            for i in range(0, len(self.queue)):
                if self.queue[i][0] == ctx.message.guild:
                    item = self.queue[i]
                    self.queue.remove(item)
                    break
            if item[0] == ctx.message.guild:                    
                voice_channel.play(item[1][0])
                current_volume = None
                for vol in self.volume:
                    if vol[0] == ctx.message.guild:
                        ctx.voice_client.source.volume = vol[1] / 100
                        current_volume = vol[1]
                if current_volume == None:
                    new_vol = [ctx.message.guild, 50]
                    self.volume.append(new_vol)
                    current_volume = new_vol[1]
                    ctx.voice_client.source.volume = new_vol[1] / 100


                emb = discord.Embed(title=':musical_note: Playing', color=discord.Color.blue())
                emb.add_field(name="Information", value=f"Requested by {item[2].mention}\nVolume: **{current_volume}%**", inline=False)
                emb.add_field(name="Song", value=f'{item[1][0].title}', inline=False)
                await send_embed(ctx, emb)

                while voice_channel.is_playing() or voice_channel.is_paused():
                    await asyncio.sleep(1)
            else:
                pass
        await voice_channel.disconnect()
        self.i = 0
        emb = discord.Embed(title='End', color=discord.Color.red())
        emb.add_field(name="Queue finished", value=f"That's everything you added!")
        await send_embed(ctx, emb)


    @commands.command(name='leave', help="Leaves the voice channel")
    async def exit_voice(self, ctx):
        try:
            await ctx.voice_client.disconnect()
            await ctx.send("Sucessfully left the voice channel")
            if len(self.queue) > 0:
                self.queue = []
        except Exception as e:
            print(e)
            await ctx.send(f"ERROR: {ctx.message.author.mention} Something went wrong!")


    @commands.command(name='skip', help="Skips the current song")
    async def skip_music(self, ctx):
        
        if self.i == 4:
            self.i = 3
        try:
            await ctx.send(self.skipping[self.i])
            ctx.voice_client.stop()
            self.i += 1
        except:
            await ctx.send("Something went wrong skipping the song!")


    @commands.command(name='pause', help="pauses the music")
    async def pause_music(self, ctx):
        try:
            ctx.voice_client.pause()
            await ctx.send("Pausing music")
        except:
            await ctx.send("Something went wrong pausing the song")


    @commands.command(name='resume', help="Resumes playing music")
    async def resume_music(self, ctx):
        try:
            ctx.voice_client.resume()
            await ctx.send("Resuming music")
        except:
            await ctx.send("Something went wrong resuming the song!")


    @commands.command(name="volume", aliases=['v', 'vol', 'VOL', 'VOLUME', 'V'], help="Sets the volume for MEXAM (values from 0-100) usage: .volume (shows current volume) / .volume <number> (sets volume to <number>%)")
    async def volume_set(self, ctx, value=-1):
        try:
            if value == -1:
                for vol in self.volume:
                    if vol[0] == ctx.message.guild:
                        await ctx.send(f"Volume is currently at {vol[1]}%")
                        break
                return

            if len(self.volume) == 0:
                self.volume.append([ctx.message.guild, value])
            ctx.voice_client.source.volume = int(value) / 100
            for vol in self.volume:
                if vol[0] == ctx.message.guild:
                    vol[1] = value
            await ctx.send(f"Volume set to {value}%")
        except:
            await ctx.send("Something went wrong setting the volume!")


    @commands.command(name='yt', help="Play Songs from Youtube!\nUsage: .yt <song> <volume> (Volume [0-100] is optional)")
    async def play(self, ctx, *, input):
        try:
            vol=0.5
            if ctx.author.voice == None:
                await ctx.send(f":x: {ctx.author.mention}, you're not in a voice channel!")
                return 
            
            channel = ctx.author.voice.channel
            voice_channel = discord.utils.get(self.bot.voice_clients, guild=ctx.message.guild)
            if voice_channel is None:
                voice_channel = await channel.connect()

            try:
                vol = int(input[1]) / 100
                input = input[0]
            except:
                pass
            song = None
            if "youtube.com" in input:
                song = await YTDLSource.from_url(input, loop=self.bot.loop, volume=vol)
            else:
                song = await YTDLSource.from_text(input, loop=self.bot.loop, volume=vol)
            if song == None:
                await ctx.send(f":x: Failed to find or download {input}")        
                return

            self.queue.append((ctx.message.guild, song, ctx.message.author))
            if not voice_channel.is_playing() and not voice_channel.is_paused():
                await self.play_queue(ctx, voice_channel)
            else:
                emb = discord.Embed(title=':musical_note: Added to queue', color=discord.Color.green())
                emb.add_field(name="Information", value=f"Requested by {ctx.message.author.mention}", inline=False)
                emb.add_field(name="Song", value=f'{song[0].title}', inline=False)
                await send_embed(ctx, emb)

        except Exception as e:
            print(e)
            await ctx.send(f"{e.args}!")


    @commands.command(name='queue', help="Shows the current youtube queue")
    async def queue_show(self, ctx):
        songs = ""
        count = 0
        emb = discord.Embed(title='Queue', color=discord.Color.green())
        for i, j, k in self.queue:
            if ctx.message.guild == i:
                count += 1
                songs += "**" + str(count) + ".** " + j[0].title + ", requested by " + k.mention + "\n\n"
        if count == 0:
            await ctx.send("No songs in queue!")
        else:
            emb.add_field(name="Songs", value=songs, inline=False)
            await send_embed(ctx, emb)


    @commands.command(name='clear-queue', aliases=['qcls', 'qclear', 'clear'], help="Clears the current queue")
    async def clear_queue(self, ctx):
        for i in range(len(self.queue) - 1, -1, -1):
            if ctx.message.guild == self.queue[i][0]:
                os.system("rm -r " + self.queue[i][1][1])
                self.queue.remove(self.queue[i])
        await ctx.send("Queue cleared! :sunglasses:")