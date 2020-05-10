import discord
import random
from discord.ext import commands
from bot_data_functions import *
from bot_commands import *


client = commands.Bot(command_prefix = ".")

        
@client.event
async def on_ready():
        loadPlayerData()
        print("bot is ready")
        # channel = client.get_channel(707749690396901508)
        # command testing channel
        # await channel.send("Bot Restarted.")
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
async def gay(ctx):
        await ctx.send(ctx.message.author.mention + " is gay :)")


@client.command()
async def commands(ctx):
        string1 = "To input your SR, please use the following commands:\n.tank <SR>"
        string2 = "\n.dps <SR>\n.support <SR>\n\nTo see your SR, use .sr\n"
        string3 = "To queue for a role, use .q <role>\nTo see the current queue, use .q"
        string3_5 = "\nTo see the roles needed to make a match, use .roles"
        string4 = "\n\nTo begin matchmaking, use .mm\n\nTo report the winning team, "
        string5 = "use .win <1/2>\nIn case of a tie, use .win 0"
        await ctx.send(string1 + string2 + string3 + string3_5
                       + string4 + string5)

        
@client.command(aliases=["matchmake"])
async def mm(ctx):
        mylist = getAllPlayerData()
        matchList = matchmake(mylist)
        if matchList[0] == -1:
                await ctx.send("Not enough players queued.")
        else:
                await ctx.send(printTeams(matchList))
                savePlayerData(matchList[0])
        

@client.command(aliases=["w"])
async def win(ctx):
        if ctx.message.content[-1:] != "0":
                await ctx.send("Congrats Team " + ctx.message.content[-1:])
        else:
                await ctx.send("My algorithm is so good, t"
                               "he teams were perfectly balanced.")
        adjust(int(ctx.message.content[-1:]))


##@client.command(aliases=["testmatchmake"])
##async def testmm(ctx):
##        mylist = matchmakeData()
##        matchList = matchmake(mylist)
##        if matchList == -1:
##                await ctx.send("Not enough players queued.")
##        else:
##                await ctx.send(printTeams(matchList))


@client.command(aliases=["support", "supp", "tank", "damage", "dps"])
async def update(ctx):
        mystr = ctx.message.content
        sender = str(ctx.message.author)
        if updatePlayerData(mystr, sender):
                await ctx.send("Added!")
        else:
                await ctx.send("Please enter a valid integer.")


@client.command(aliases=["q"])
async def queue(ctx, role="none"):
        if role == "none":
                await ctx.send(ctx.message.author.mention + "\n" + printQueue())
        else:
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
        
        
@client.command(aliases=["l"])
async def leave(ctx):
        sender = str(ctx.message.author)
        message = deQueue(sender)
        print(message)
        message = message + "Roles Needed:\n"
        if tankQueued() != 0:
                message = message + (tankQueued() + " tanks.\n")
        if dpsQueued() != 0:
                message = message + (dpsQueued() + " dps.\n")
        if suppQueued() != 0:
                message = message + (suppQueued() + " supports.\n")
        if allQueued():
                message = "All roles filled."
        await ctx.send(message)


@client.command(aliases=["SR"])
async def sr(ctx):
        try:
                sender = str(ctx.message.author)
                sr = printPlayerData(sender)
                await ctx.send(sr)
        except:
                await ctx.send("Error 404: SR doesn't exist")


@client.command()
async def status(ctx):
        sender = str(ctx.message.author)
        sr = printQueueData(sender)
        await ctx.send(ctx.message.author.mention + sr)


@client.command(aliases=["allsr"])
async def allSR(ctx):
        try:
                sr = printAllPlayerData()
                await ctx.send(sr)
        except:
                await ctx.send("Error 404: SR doesn't exist")
       

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


client.run("TOKEN")
