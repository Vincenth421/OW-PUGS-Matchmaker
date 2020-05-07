import discord
from discord.ext import commands
from bot_commands import *

client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
	print("Bot is ready")
	
@client.event
async def on_message(message):
    channel = message.channel
    mystr = message.content
    sender = str(message.author)
##    if mystr.startswith("!mention"):
##        await client.send_message(channel, message.author.mention)
    await client.process_commands(message)


@client.command()
async def matchmake(ctx):
        pass

@client.command(aliases=["support", "tank", "damage", "dps"])
async def update(ctx):
        mystr = ctx.message.content
        sender = str(ctx.message.author)
        updatePlayerData(mystr, sender)

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
        


client.run("TOKEN")
