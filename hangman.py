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

wordlist = None

with open("wordlist.txt", "r") as file:
    wordlist = file.readlines()

for i in range(len(wordlist)):
    wordlist[i] = wordlist[i].rstrip('\n')

class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.player = None
        self.word = None
        self.guessed_word = []
        self.tries = 10
        self.used = []

    @commands.command(name="hang-create", aliases=['hc'], help="Creates a new Hangman Game for a specific player")
    async def hangman_create(self, ctx):
        if self.player is None or self.player == ctx.message.author:
            self.player = ctx.message.author
            self.word = wordlist[random.randint(0, len(wordlist))]
            for i in range(len(self.word)):
                self.guessed_word.append('- ')
            await ctx.send("Your word is " + ''.join(self.guessed_word) + "\tTries: " + str(self.tries))

    @commands.command(name='hang-guess', aliases=['hg'], help='Enter a character as a guess. (Only when you created a hangman game)')
    async def hangman_guess(self, ctx, input):
        count = 0
        if ctx.message.author == self.player:
            if self.tries > 0 and self.word != ''.join(self.guessed_word):
                if isinstance(input, str):
                    if len(input) == 1:
                        if input + " " not in self.used:
                            self.used.append(input + " ")
                        for i in range(len(self.word)):
                            if self.word[i] == input:
                                count += 1
                                self.guessed_word[i] = input
                        if count != 0 and self.word != ''.join(self.guessed_word):
                            await ctx.send("CORRECT\nYour word is " + ''.join(self.guessed_word) + "\tTries: " + str(self.tries) + "\n\nUsed Characters: " + ''.join(self.used))
                        elif count != 0 and self.word == ''.join(self.guessed_word) and self.tries > 0:
                            await ctx.send(":trophy: YOU WON! The word was " + self.word)
                            self.word = None
                            self.guessed_word = []
                            self.used = []
                            self.player = None
                            self.tries = 10
                        elif self.tries > 1:
                            self.tries -= 1
                            await ctx.send(input + " was not in the word..\nYour word is " + ''.join(self.guessed_word) + "\tTries: " + str(self.tries) + "\n\nUsed Characters: " + ''.join(self.used))
                        else:
                            self.tries -= 1
                            await ctx.send(":no_entry: YOU LOST! The word was " + self.word)
                            self.word = None
                            self.guessed_word = []
                            self.used = []
                            self.player = None
                            self.tries = 10
                    else:
                        await ctx.send("```Please enter only one character!```")
    
