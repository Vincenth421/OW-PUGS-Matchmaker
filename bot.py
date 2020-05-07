import discord
import random
from discord.ext import commands
from bot_commands import *

client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
        # loadPlayerData()
        print("bot is ready")

@client.event
async def on_message(message):
    channel = message.channel
    mystr = message.content
    sender = str(message.author)
    await client.process_commands(message)


@client.command()
async def mention(ctx):
        await ctx.send(ctx.message.author.mention)

        
@client.command()
async def matchmake(ctx):
        await ctx.send("this doesn't work yet, you fool")

@client.command(aliases=["support", "tank", "damage", "dps"])
async def update(ctx):
        mystr = ctx.message.content
        sender = str(ctx.message.author)
        updatePlayerData(mystr, sender)
        await ctx.send("Added!")

@client.command()
async def sr(ctx):
        sender = str(ctx.message.author)
        sr = getPlayerData(sender)
        await ctx.send(sr)

@client.command()
async def clear(ctx, amount=1):
        if amount > 0:
                await ctx.channel.purge(limit=amount+1)

@client.command()
async def author(ctx):
        await ctx.send(ctx.message.author)

@client.command(aliases=["coin"])
async def flip(ctx):
        result = random.randint(0,1)
        if result == 0:
                await ctx.send("Heads!")
        else:
                await ctx.send("Tails!")


client.run("TOKEN")
