import discord
import random
from discord.ext import commands
from bot_data_functions import *
from bot_commands import *
from discord import ChannelType
import asyncio
import datetime

client = commands.Bot(command_prefix = ".")


@client.event
async def on_ready():
        ''' Prints a message when the bot is ready.
        '''
        loadPlayerData()
        print("bot is ready")


@client.command(aliases=["pugs"])
@commands.has_role('Scheduler')
async def schedule(ctx, time, metric):
        now = datetime.datetime.now()
        sleep_timer = 0
        
        if metric.lower() == "s":
                sleep_timer = int(time)
        elif metric.lower() == "m":
                sleep_timer = int(time) * 60
        elif metric.lower() == "h":
                sleep_timer = int(time) * 60 * 60
        
        for i in ctx.message.guild.roles:
                if str(i) == "Puggers":
                        role = i
        pugs_time = (now +
                     datetime.timedelta(seconds =
                                        sleep_timer)).strftime("%H:%M")
        try:
                poll = await ctx.send(
                                      ", react if you're down " +
                                      "for pugs at " + pugs_time +
                                      " PST.")
        except:
                poll = await ctx.send("React if you're down for pugs" +
                                      " at " + pugs_time + " PST.")
           
        check = '✅'
        await poll.add_reaction(check)
          
        await asyncio.sleep(sleep_timer)

        try:
                cache_poll = await ctx.fetch_message(poll.id)
                
                num_puggers = 0
                for reaction in cache_poll.reactions:
                        if str(reaction) == check:
                                num_puggers = reaction.count - 1

                if num_puggers > 12:
                        try:
                                await ctx.send(
                                       " the time for pugs is upon us!")
                        except:
                                await ctx.send("It's pugs time!")
                else:
                        await ctx.send("Not enough people responded." +
                                       " Please get " +
                                       str(12-num_puggers) + " more.")
        except:
                await ctx.send("A scheduling error occured. "
                               "Was the original message deleted?")

        
##@client.event
##async def on_message(message):
##    channel = message.channel
##    mystr = message.content
##    sender = str(message.author)
##    await client.process_commands(message)


@client.command()
async def shock(ctx):
        await ctx.send("Shock did it without sinatraa fuck all " +
                       "yall that doubted and said super is a benched player."
                       + " Thank you for reading my PSA have a good night see "
                       + "you guys for pugs")



@client.command(aliases=["mtt"])
#@commands.has_role('BotMaster')
async def move_to_teams(ctx):
        ''' Moves people on teams to the specific team channel from the draft
                channel.
        '''
        if ctx.message.author.id == 176510548702134273:
                try:
                        ## ## MatchMaking Bot Testing channel IDs
                        if ctx.message.guild.id == 651200164169777154:
                                draft_channel = client.get_channel(709248862828888074)
                                channel1 = client.get_channel(707749575108198441)
                                channel2 = client.get_channel(707749630728732712)

                        ## ## We Use this channel IDs
                        if ctx.message.guild.id == 442813167148728330:
                                draft_channel = client.get_channel(652717496045928458)
                                channel1 = client.get_channel(647667378334990377)
                                channel2 = client.get_channel(647667443782909955)
                        
                        pdata = loadPlayerData()
                        team1 = get_t1_id(pdata)
                        team2 = get_t2_id(pdata)
                        sender = ctx.message.author
                        num_moved = 0
                        for member in ctx.message.guild.members:
                                if member.id in team1:
                                        if member in draft_channel.members:
                                                await member.move_to(channel1)
                                                num_moved += 1
                                elif member.id in team2:
                                        if member in draft_channel.members:                                                await member.move_to(channel2)
                                        num_moved += 1
                        #await ctx.send("{} users moved.".format(num_moved))
                except:
                        await ctx.send("You do not have permission to use this command.")

@client.command(aliases=["mtd"])
#@commands.has_role('BotMaster')
async def move_to_draft(ctx):
        ''' Moves all users from the team channels to the draft channel.
        '''
        if ctx.message.author.id == 176510548702134273:
                ## ## MatchMaking Bot Testing channel IDs
                if ctx.message.guild.id == 651200164169777154:
                        draft_channel = client.get_channel(709248862828888074)
                        channel1 = client.get_channel(707749575108198441)
                        channel2 = client.get_channel(707749630728732712)

                ## ## We Use this channel IDs
                if ctx.message.guild.id == 442813167148728330:
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
                #await ctx.send("{} users moved.".format(num_moved))


@client.command()
async def captains(ctx):
        ## ## MatchMaking Bot Testing channel IDs
        if ctx.message.guild.id == 651200164169777154:
                draft_channel = client.get_channel(709248862828888074)

        ## ## We Use this channel IDs
        if ctx.message.guild.id == 442813167148728330:
                draft_channel = client.get_channel(652717496045928458)

        print(draft_channel.members)
        i = random.randint(0, len(draft_channel.members))
        j = random.randint(0, len(draft_channel.members))
        while i == j:
                j = random.randint(0, len(draft_channel.members))
        await ctx.send(draft_channel.members[i].mention + " " +
                       draft_channel.members[j].mention +
                       " are your captains.")


@client.command()
async def team(ctx):
        ''' Reminds the sender what team they're on.
        '''
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
        ''' Sends a random map.
        '''
        if str(ctx.message.author) == "TheGlare#1451":
                await ctx.send("King's Row")
        else:
                await ctx.send(randomMap())


@client.command()
async def mention(ctx):
        ''' Mentions whoever used the command.
        '''
        await ctx.send(ctx.message.author.mention)


@client.command(aliases = ["dick", "size"])
async def dicksize(ctx):
        ''' Randomly assigns a number in inches, specific users have earned a
                modifier.
        '''
        i = random.randint(321, 987)
        if str(ctx.message.author) == "Panda#3239":
                i += 2000
                message = "dick?"#str(i/100) + " nanometer dick."
        elif str(ctx.message.author) == "Timmy#3426":
                i += 30
                message = str(i/100) + " inch dick."
        elif str(ctx.message.author) == "Twang#8757":
                i -= 321
                message = str(i/100) + " inch dick."
        elif str(ctx.message.author) == "StodgyMeteor#8420":
                i -= 250
                message = str(i/100) + " inch dick."
        elif str(ctx.message.author) == "Archangel#0346":
                i += 850
                message = str(i/100) + " inch dick."
        elif str(ctx.message.author) == "Aries#0666":
                i -= 321
                message = str(i/100) + " yard dick."
        elif str(ctx.message.author) == "BubbLeS#4835":
                message = "dick beyond human comprehension."
        else:
                message = str(i/100) + " inch dick."
##                await ctx.send(ctx.message.author.mention +
##                               " has a massive dick.")
        #else:
        await ctx.send(ctx.message.author.mention + " has a "
                       + message)


@client.command(aliases=["bi", "pan"])
async def gay(ctx):
        ''' Randomly assigns the user a sexuality. Not always random.
        '''
        i = random.randint(0,100)
        if str(ctx.message.author) == "Aries#0666":
                await ctx.send(ctx.message.author.mention + " is a mercy main.")
        elif str(ctx.message.author) == "Panda#3239":
                await ctx.send(ctx.message.author.mention + " is bi.")
        elif str(ctx.message.author) == "StodgyMeteor#8420":
                await ctx.send(ctx.message.author.mention + " is a bad torb.")
        else:
                if (i % 11) == 0:
                        await ctx.send(ctx.message.author.mention +
                                       " is gay.")
                elif (i % 11) == 1:
                        await ctx.send(ctx.message.author.mention +
                                       " is straight.")
                elif (i % 11) == 2:
                        await ctx.send(ctx.message.author.mention +
                                       " is asexual.")
                elif (i % 11) == 3:
                        await ctx.send(ctx.message.author.mention +
                                       " is bi.")
                elif (i % 11) == 4:
                        await ctx.send(ctx.message.author.mention +
                                       " is closeted :0.")
                elif (i % 10) == 5:
                        await ctx.send(ctx.message.author.mention +
                                       " just came out!")
                elif (i % 11) == 6:
                        await ctx.send(ctx.message.author.mention +
                                       " is pan.")
                elif (i % 11) == 7:
                        await ctx.send(ctx.message.author.mention +
                                       " is sexy af.")
                elif (i % 11) == 8:
                        await ctx.send(ctx.message.author.mention +
                                       " will probably die alone :(")
                elif (i % 11) == 9:
                        await ctx.send(ctx.message.author.mention +
                                       " Error 404: Sexuality not found.")
                elif (i % 11) == 10:
                        await ctx.send(ctx.message.author.mention +
                                       " is a furry.")


@client.command()
async def commands(ctx):
        ''' Prints working commands.
        '''
        string1 = """To input your SR, please use the following commands:
        \n.tank SR\n.dps SR\n.support SR
        \nTo see your SR, use .sr
        \nTo queue for a role, use .q role\nTo see the current queue, use .q
        \nTo see what you are queued for, use .status
        \nTo see the roles needed to make a match, use .roles
        \nTo begin matchmaking, use .mm
        \nTo report the winning team, use.win 1/2
        \nIn case of a tie, use .win 0"""
        """
        \nTo move users to team channels after matchmaking, use .mtt
        \nTo move users from team channels back to draft, use .mtd
        """
        await ctx.send(string1)

        
@client.command(aliases=["matchmake"])
async def mm(ctx):
        ''' Makes a match based on users queued. If not enough players
                are queued prints an error message.
        '''
        mylist = getAllPlayerData()
        matchList = matchmake(mylist)
        if matchList[0] != -1:
                await ctx.send(printTeams(matchList))
                await client.change_presence(activity=discord.Game(name="a match"))
                savePlayerData(matchList[0])
                await ctx.send(randomMap())
        else:
                await ctx.send("Error encountered. Are enough players queued?")
        
        

@client.command(aliases=["w"])
async def win(ctx):
        ''' Calls adjust to add or subtract player SR.
        '''
        adjust(int(ctx.message.content[-1:]))
        if ctx.message.content[-1:] != "0":
                await ctx.send("Congrats Team " + ctx.message.content[-1:])
        else:
                await ctx.send("My algorithm is so good, t"
                               "he teams were perfectly balanced.")
        clearQueue()
        await client.change_presence(activity=discord.Game(name=""))


@client.command(aliases=["support", "supp", "tank", "damage", "dps"])
async def update(ctx):
        ''' Updates the dictionary of player data with the new data.
        '''
        mystr = ctx.message.content
        sender = str(ctx.message.author)
        discord_id = ctx.message.author.id
        if updatePlayerData(mystr, sender, discord_id):
                await ctx.send("Added!")
        else:
                await ctx.send("Please enter a valid integer.")


@client.command(aliases=["q"])
async def queue(ctx, role="none"):
        ''' If no args passed, prints the queue. Else it updates the
                sender's data to place them in the queue for what role
                they want.
        '''
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
        ''' Prints out the roles needed to matchmake.
        '''
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
        ''' Leaves the queue.
        '''
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
        ''' Prints out the player's saved SR values.
        '''
        try:
                sender = str(ctx.message.author)
                sr = printPlayerData(sender)
                await ctx.send(sr)
        except:
                await ctx.send("Error 404: SR doesn't exist")


@client.command()
async def status(ctx):
        ''' Prints what the user is queued for.
        '''
        sender = str(ctx.message.author)
        sr = printQueueData(sender)
        await ctx.send(ctx.message.author.mention + sr)


@client.command(aliases=["allsr"])
async def allSR(ctx):
        ''' Prints out all the saved SR data.
        '''
        try:
                sr = printAllPlayerData()
                await ctx.send(sr)
        except:
                await ctx.send("Error 404: SR doesn't exist")
       

@client.command()
async def clear(ctx, amount=5):
        ''' Removes a specified amount of messages.
        '''
        if amount > 0:
                await ctx.channel.purge(limit=amount+1)


@client.command(aliases=["coin"])
async def flip(ctx):
        ''' Flips a coin.
        '''
        result = random.randint(0,1)
        if result == 0:
                await ctx.send("Heads!")
        else:
                await ctx.send("Tails!")


client.run("NzA3NzI0OTUzMzUyNTM2MTU2.XtMTXQ.ibFU_ubrKjpxi4LTKMnLnDeka2w")
