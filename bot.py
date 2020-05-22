import discord
import random
from discord.ext import commands
from bot_data_functions import *
from bot_commands import *
from discord import ChannelType

client = commands.Bot(command_prefix = ".")


@client.event
async def on_ready():
        loadPlayerData()
        print("bot is ready")
        # channel = client.get_channel(708912394537009152)
        # command testing channel
        # await channel.send("I'm getting bullied so y'all gotta do draft.")
        # print(clearPlayerData())


##@client.event
##async def on_message(message):
##    channel = message.channel
##    mystr = message.content
##    sender = str(message.author)
##    await client.process_commands(message)


@client.command(aliases=["mtt"])
async def move_to_teams(ctx):
        draft_channel = client.get_channel(709248862828888074)
        channel1 = client.get_channel(707749575108198441)
        channel2 = client.get_channel(707749630728732712)
        pdata = loadPlayerData()
        team1 = get_t1_id(pdata)
        team2 = get_t2_id(pdata)
        sender = ctx.message.author
        #print(type(sender))
        #await sender.move_to(channel2)
        num_moved = 0
        for member in ctx.message.guild.members:
                if member.id in team1:
                        if member in draft_channel.members:
                                await member.move_to(channel1)
                                num_moved += 1
                elif member.id in team2:
                        if member in draft_channel.members:
                                await member.move_to(channel2)
                                num_moved += 1
        await ctx.send("{} users moved.".format(num_moved))

@client.command(aliases=["mtd"])
async def move_to_draft(ctx):
        ## ## MatchMaking Bot Testing channel IDs
        #draft_channel = client.get_channel(709248862828888074)
        #channel1 = client.get_channel(707749575108198441)
        #channel2 = client.get_channel(707749630728732712)

        ## ## We Use this channel IDs
        draft_channel = client.get_channel(652717496045928458)
        channel1 = client.get_channel(647667378334990377)
        channel2 = client.get_channel(647667443782909955)
        num_moved = 0
        for member in channel1.members:
                await member.move_to(draft_channel)
                num_moved += 1
        for member in channel2.members:
                await member.move_to(draft_channel)
                num_moved += 1
        await ctx.send("{} users moved.".format(num_moved))


@client.command()
async def ping(ctx):
    await ctx.send("MatchMaker Bot's Ping: {0}".format(round(client.latency, 2)))


@client.command()
async def team(ctx):
        sender = str(ctx.message.author)
        team = getPlayerTeam(sender)
        if team == "-1":
                await ctx.send(ctx.message.author.mention +
                               ", you're not on a team.")
        else:
                await ctx.send(ctx.message.author.mention +
                               ", you're on team " + str(team))


@client.command(aliases=["randomMap", "randommap"])
async def map(ctx):
        await ctx.send(randomMap())


@client.command()
async def mention(ctx):
        await ctx.send(ctx.message.author.mention)


@client.command(aliases = ["dick", "size"])
async def dicksize(ctx):
        i = random.randint(300, 1200)
        if str(ctx.message.author) == "Panda#3239":
                i += 800
        elif str(ctx.message.author) == "Timmy#3426":
                i -= 300
        elif str(ctx.message.author) == "Twang#8757":
                i += 500
        #        await ctx.send(ctx.message.author.mention + " has a massive dick.")
        #else:
        await ctx.send(ctx.message.author.mention + " has a "
                       + str(i/100) + " inch dick.")


@client.command(aliases=["bi", "pan"])
async def gay(ctx):
        i = random.randint(0,89)
        if str(ctx.message.author) == "Aries#666":
                await ctx.send(ctx.message.author.mention + " ain't sexy at all.")
        elif str(ctx.message.author) == "Panda#3239":
                await ctx.send(ctx.message.author.mention + "is bi.")
        elif str(ctx.message.author) == "StodgyMeteor#8420":
                await ctx.send(ctx.message.author.mention + "is a bad torb.")
        else:
                if (i % 9) == 0:
                        await ctx.send(ctx.message.author.mention +
                                       " is gay.")
                elif (i % 9) == 1:
                        await ctx.send(ctx.message.author.mention +
                                       " is straight.")
                elif (i % 9) == 2:
                        await ctx.send(ctx.message.author.mention +
                                       " is asexual.")
                elif (i % 9) == 3:
                        await ctx.send(ctx.message.author.mention +
                                       " is bi.")
                elif (i % 9) == 4:
                        await ctx.send(ctx.message.author.mention +
                                       " is closeted :0.")
                elif (i % 9) == 5:
                        await ctx.send(ctx.message.author.mention +
                                       " just came out!")
                elif (i % 9) == 6:
                        await ctx.send(ctx.message.author.mention +
                                       " is pan.")
                elif (i % 9) == 7:
                        await ctx.send(ctx.message.author.mention +
                                       " is sexy af.")
                elif (i % 9) == 8:
                        await ctx.send(ctx.message.author.mention +
                                       " will probably die alone :(")
                elif (i % 9) == 9:
                        await ctx.send(ctx.message.author.mention +
                                       " Error 404: Sexuality not found.")


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
        if matchList[0] != -1:
                await ctx.send(printTeams(matchList))
                savePlayerData(matchList[0])
        else:
                await ctx.send("Error encountered. Are enough players queued?")
        
        

@client.command(aliases=["w"])
async def win(ctx):
        adjust(int(ctx.message.content[-1:]))
        if ctx.message.content[-1:] != "0":
                await ctx.send("Congrats Team " + ctx.message.content[-1:])
        else:
                await ctx.send("My algorithm is so good, t"
                               "he teams were perfectly balanced.")
        clearQueue()


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
        discord_id = ctx.message.author.id
        if updatePlayerData(mystr, sender, discord_id):
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


@client.command(aliases=["role"])
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
