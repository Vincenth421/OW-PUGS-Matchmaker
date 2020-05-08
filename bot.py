import discord
import random
from discord.ext import commands
from bot_data_functions import *
from bot_commands import *

client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
        loadPlayerData()
        print("bot is ready")
        channel = client.get_channel(707749690396901508)
        # command testing channel
        await channel.send("Bot Restarted.")
        # print(clearPlayerData())

##@client.event
##async def on_message(message):
##    channel = message.channel
##    mystr = message.content
##    sender = str(message.author)
##    await client.process_commands(message)

        
@client.command()
async def ping(ctx):
    await ctx.send("MatchMaker Bot's Ping: {0}".format(round(client.latency, 2)))

@client.command(aliases=["randomMap", "randommap"])
async def map(ctx):
        await ctx.send(randomMap())

@client.command()
async def mention(ctx):
        await ctx.send(ctx.message.author.mention)


@client.command()
async def commands(ctx):
        cmds = "Working commands: mention, support, tank, damage/dps, ready, sr, clear, flip/coin"
        link = "http://blue.cs.sonoma.edu/~cholland/matchmaker.html"
        await ctx.send(cmds + "\n" + link)

        
@client.command(aliases=["matchmake"])
async def mm(ctx):
        mylist = getAllPlayerData()
        matchList = matchmake(mylist)
        if matchList == -1:
                await ctx.send("Not enough players queued.")
        else:
                await ctx.send(printTeams(matchList))
        

@client.command()
async def win(ctx):
        mylist = matchmakeData()
        newData = adjust(mylist, ctx.message.content)


@client.command(aliases=["testmatchmake"])
async def testmm(ctx):
        mylist = matchmakeData()
        matchList = matchmake(mylist)
        if matchList == -1:
                await ctx.send("Not enough players queued.")
        else:
                await ctx.send(printTeams(matchList))
        

@client.command(aliases=["support", "tank", "damage", "dps"])
async def update(ctx):
        mystr = ctx.message.content
        sender = str(ctx.message.author)
        if updatePlayerData(mystr, sender):
                await ctx.send("Added!")
        else:
                await ctx.send("Please enter a valid integer.")


@client.command(aliases=["q"])
async def queue(ctx, role):
        sender = str(ctx.message.author)
        message = (queueFor(role, sender)) + "Roles Needed:\n"
        if tankQueued() != 0:
                message = message + (tankQueued() + " tanks.\n")
        if dpsQueued() != 0:
                message = message + (dpsQueued() + " dps.\n")
        if suppQueued() != 0:
                message = message + (suppQueued() + " supports.\n")
        if message == "Roles Needed:\n":
                message = "All roles filled."
        await ctx.send(message)

@client.command()
async def roles(ctx):
        message = "Roles Needed:\n"
        if tankQueued() != 0:
                message = message + (tankQueued() + " tanks.\n")
        if dpsQueued() != 0:
                message = message + (dpsQueued() + " dps.\n")
        if suppQueued() != 0:
                message = message + (suppQueued() + " supports.\n")
        if message == "Roles Needed:\n":
                message = "All roles filled."
        await ctx.send(message)
        
        
@client.command()
async def leave(ctx):
        sender = str(ctx.message.author)
        deQueue(sender)
        message = "Left the queue.\n Roles Needed:\n"
        if tankQueued() != 0:
                message = message + (tankQueued() + " tanks.\n")
        if dpsQueued() != 0:
                message = message + (dpsQueued() + " dps.\n")
        if suppQueued() != 0:
                message = message + (suppQueued() + " supports.\n")
        if message == "Roles Needed:\n":
                message = "All roles filled."
        await ctx.send(message)


@client.command(aliases=["sr"])
async def status(ctx):
        try:
                sender = str(ctx.message.author)
                sr = getPlayerData(sender)
                await ctx.send(sr)
        except:
                await ctx.send("Error.")


@client.command(aliases=["allSR"])
async def allStatus(ctx):
        sr = getAllPlayerData()
        await ctx.send(sr)
       

@client.command()
async def clear(ctx, amount=5):
        if amount > 0:
                await ctx.channel.purge(limit=amount+1)


@client.command(aliases=["coin"])
async def flip(ctx):
        result = random.randint(0,1)
        if result == 0:
                await ctx.send("Heads!")
        else:
                await ctx.send("Tails!")


client.run("NzA3NzI0OTUzMzUyNTM2MTU2.XrN0jQ.bQzV16CNMQZ3cPSPy1F3mS-rbUo")
