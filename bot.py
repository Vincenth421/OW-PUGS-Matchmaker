import discord
import random
from discord.ext import commands
from bot_data_functions import *
from bot_matchmake_functions import *
from discord import ChannelType
import asyncio
from discord.utils import get
import datetime

client = commands.Bot(command_prefix = ".")
global game_in_progress
game_in_progress = False

global msg
global response

vip_list = ["176510548702134273", "176550035994050560", "364167513971621890",
            "238471482009714688"]

## Cameron, Michael, Tony, Panda


@client.event
async def on_ready():
        ''' Prints a message when the bot is ready.
        '''
        loadPlayerData()
        print("bot is ready")
'''
@client.event
async def on_message(message):
        if str(message.guild.id) == "651200164169777154":
                pass
        else:
                await client.process_commands(message)
'''

@client.command()
async def vip(ctx):
        global vip_list
        if str(ctx.message.author.id) == "176510548702134273":
                vip_list.append(str(ctx.message.mentions[0].id))


@client.command(aliases=["btag", "tag"])
async def battletag(ctx, btag):
        if setBtag(btag, str(ctx.message.author), ctx.message.author.id):
                await ctx.send(ctx.message.author.mention +
                               ", your battletag has been saved. " +
                               "Use .update to pull data from Overwatch " +
                               "after ensuring your profile is public.")
        else:
                await ctx.send(ctx.message.author.mention +
                               ", something went wrong.")


@client.command()
async def update(ctx):
        ''' Updates the player data based off their in game profile.
        '''
        await ctx.send("This may take a while and will pause all " +
                       "other commands. Please be patient and do not spam it.")
        
        if pullSR(str(ctx.message.author), ctx.message.author.id):
                await ctx.send(ctx.message.author.mention +
                               ", success! Your data has been imported." +
                               " If you are not placed or not public, data" +
                               " will not be overwritten.")
        else:
                await ctx.send(ctx.message.author.mention +
                               ", something went wrong. Is your profile " +
                               "public and have you completed any placements?")

        
@client.command(aliases=["pugs"])
async def schedule(ctx, time, metric):
        ''' Schedules a pug event some time in the future.
        '''
        if str(ctx.message.author.id) in vip_list:
                # await ctx.message.delete()
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
                try:
                        poll = await ctx.send(role.mention +
                                              ", react if you're down " +
                                              "for pugs in " + time + metric)
                except:
                        poll = await ctx.send("React if you're down for pugs in "
                                              + time + metric)
                   
                check = '✅'
                rart = 'Rart:658615209463775242'
                await poll.add_reaction(rart)
                  
                await asyncio.sleep(sleep_timer)

                try:
                        cache_poll = await ctx.fetch_message(poll.id)
                        
                        num_puggers = 0
                        for reaction in cache_poll.reactions:
                                print(str(reaction))
                                if str(reaction) == "<:Rart:658615209463775242>":
                                        num_puggers = reaction.count - 1

                        if num_puggers > 12:
                                try:
                                        await ctx.send(role.mention +
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
        ''' Shock
        '''
        # await ctx.message.delete()
        await ctx.send("Shock did it without sinatraa fuck all " +
                       "yall that doubted and said super is a " +
                       "benched player. Thank you for reading my " +
                       "PSA have a good night see you guys for pugs")



@client.command(aliases=["mtt"])
#@commands.has_role('BotMaster')
async def move_to_teams(ctx):
        ''' Moves people on teams to their respective team channel.
        '''
        # await ctx.message.delete()
        if str(ctx.message.author.id) in vip_list:
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
##                                        await member.edit(voice_channel=channel1)
                                        num_moved += 1
                        elif member.id in team2:
                                if member in draft_channel.members:
                                        await member.move_to(channel2)
##                                        await member.edit(voice_channel=channel2)
                                        num_moved += 1
                await ctx.send("{} users moved.".format(num_moved),
                               delete_after=3)


@client.command(aliases=["mtd"])
#@commands.has_role('BotMaster')
async def move_to_draft(ctx):
        ''' Moves all users from the team channels to the draft channel.
        '''
        # await ctx.message.delete()
        if str(ctx.message.author.id) in vip_list:
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
##                        await member.edit(voice_channel=draft_channel)
                        num_moved += 1
                for member in channel2.members:
                        await member.move_to(draft_channel)
##                        await member.edit(voice_channel=draft_channel)
                        num_moved += 1
                await ctx.send("{} users moved.".format(num_moved),
                               delete_after=3)


@client.command()
async def captains(ctx):
        ''' Picks two users at random from draft channel.
        '''
        ## ## MatchMaking Bot Testing channel IDs
        if ctx.message.guild.id == 651200164169777154:
                draft_channel = client.get_channel(709248862828888074)

        ## ## We Use this channel IDs
        if ctx.message.guild.id == 442813167148728330:
                draft_channel = client.get_channel(652717496045928458)

        i = random.randint(0, len(draft_channel.members))
        j = random.randint(0, len(draft_channel.members))
        while i == j:
                j = random.randint(0, len(draft_channel.members))
        await ctx.send(draft_channel.members[i].mention + " " +
                       draft_channel.members[j].mention +
                       " are your captains.", delete_after=10)


@client.command()
async def team(ctx):
        ''' Reminds the sender what team they're on.
        '''
        sender = str(ctx.message.author)
        team = getPlayerTeam(sender)
        if team == "-1":
                await ctx.send(ctx.message.author.mention +
                               ", you're not on a team.", delete_after=15)
        else:
                await ctx.send(ctx.message.author.mention +
                               ", you're on team " + str(team), delete_after=15)


@client.command(aliases=["randomMap", "randommap"])
async def map(ctx):
        ''' Sends a random map.
        '''
        if str(ctx.message.author) == "TheGlare#1451" or \
		   str(ctx.message.author) == "Archangel#0346":
                # await ctx.message.delete()
                await ctx.send("King's Row")
        else:
                await ctx.send(randomMap())


@client.command()
async def mention(ctx):
        ''' Mentions whoever used the command.
        '''
        # await ctx.message.delete()
        sleep_timer = random.randint(1, 120)
        print(sleep_timer)
        await asyncio.sleep(sleep_timer)
        await ctx.send(ctx.message.author.mention, delete_after=10)


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
        #await ctx.message.delete()
        global game_in_progress
        mylist = getAllPlayerData()
        matchList = matchmake(mylist)
        if matchList[0] != -1:
                await ctx.send(printTeams(matchList))
                await client.change_presence(activity=discord.Game(name="a match"))
                savePlayerData(matchList[0])
                await ctx.send(randomMap())
                game_in_progress = True
        else:
                await ctx.send("Error encountered. Are enough players queued?")
        

@client.command(aliases=["w"])
async def win(ctx, team_num):
        ''' Calls adjust to add or subtract player SR.
        '''
        global game_in_progress
        if (team_num == "0" or team_num == "1" or team_num == "2") \
           and game_in_progress:
                adjust(int(team_num))
                if team_num != "0":
                        await ctx.send("Congrats Team " +
                                       team_num)
                else:
                        await ctx.send("My algorithm is so good, " +
                                       "the teams were perfectly balanced.")
                clearQueue()
                await client.change_presence(activity=discord.Game(name=""))
                game_in_progress = False
        else:
                if(game_in_progress):
                        await ctx.send("Please enter a valid team.")
                else:
                      await ctx.send("No game in progress.")


@client.command(aliases=["supp"])
async def support(ctx, SR):
        ''' Updates the sender's profile with the new support data.
        '''
        sender = str(ctx.message.author)
        discord_id = ctx.message.author.id
        if setSupport(SR, sender, discord_id):
                await ctx.send(ctx.message.author.mention +
                               ", your support SR has been updated.")
        elif int(SR) <= 1000:
                await ctx.send(ctx.message.author.mention +
                               ", please rank up and try again.")
        else:
                await ctx.send(ctx.message.author.mention +
                               ", please enter a valid integer.")

@client.command(aliases=["dps"])
async def damage(ctx, SR):
        ''' Updates the sender's profile with the new dps data.
        '''
        sender = str(ctx.message.author)
        discord_id = ctx.message.author.id
        if setDamage(SR, sender, discord_id):
                await ctx.send(ctx.message.author.mention +
                               ", your dps SR has been updated.")
        elif int(SR) <= 1000:
                await ctx.send(ctx.message.author.mention +
                               ", please rank up and try again.")
        else:
                await ctx.send(ctx.message.author.mention +
                               ", please enter a valid integer.")

@client.command()
async def tank(ctx, SR):
        ''' Updates the sender's profile with the new tank data.
        '''
        sender = str(ctx.message.author)
        discord_id = ctx.message.author.id
        if (not SR.isalpha()) and setTank(SR, sender, discord_id):
                await ctx.send(ctx.message.author.mention +
                               ", your tank SR has been updated.", delete_after=15)
        elif int(SR) <= 1000:
                await ctx.send(ctx.message.author.mention +
                               ", please rank up and try again.", delete_after=15)
        else:
                await ctx.send(ctx.message.author.mention +
                               ", please enter a valid integer.", delete_after=15)


@client.command(aliases=["q"])
async def queue(ctx, role="none"):
        ''' If no args passed, prints the queue. Else it updates the
                sender's data to place them in the queue for what role
                they want.
        '''
        if game_in_progress:
                await ctx.send("Please report a winner before queuing!", delete_after=15)
        else:
                if role == "none":
                        await ctx.send(ctx.message.author.mention
                                       + "\n" + printQueue()),
                                       delete_after=15)
                elif role == "clear":
                        clearQueue()
                        await ctx.send("The queue has been emptied.", delete_after=15)
                elif role == "fill":
                        roles_needed = []
                        if suppQueued() != 0:
                                roles_needed.append("support")
                        if tankQueued() != 0:
                                roles_needed.append("tank")
                        if dpsQueued() != 0:
                                roles_needed.append("dps")
                        if len(roles_needed) == 0:
                                roles_needed = ["tank", "support", "dps"]
                        
                        rand = random.randint(0, len(roles_needed)-1)
                        sender = str(ctx.message.author)
                        message = (queueFor(roles_needed[rand], sender))
                        await ctx.send(ctx.message.author.mention + ", " +
                                       message)
                        await roles(ctx, 10)
                        
                else:
                        sender = str(ctx.message.author)
                        message = (queueFor(role, sender))
                        await ctx.send(ctx.message.author.mention + ", " +
                                       message, delete_after=25)
                        await roles(ctx, 10)


@client.command(aliases=["role"])
async def roles(ctx, timer=25):
        ''' Prints out the roles needed to matchmake.
        '''
        # await ctx.message.delete()
        message = "Roles Needed:\n"
        if tankQueued() != 0:
                message = message + (tankQueued() + " tanks.\n")
        if dpsQueued() != 0:
                message = message + (dpsQueued() + " dps.\n")
        if suppQueued() != 0:
                message = message + (suppQueued() + " supports.\n")
        if message == "Roles Needed:\n":
                message = "All roles filled."
        await ctx.send(message, delete_after=timer)
        
        
@client.command(aliases=["l"])
async def leave(ctx):
        ''' Leaves the queue.
        '''
        sender = str(ctx.message.author)
        message = deQueue(sender)
        await roles(ctx, 10)


@client.command(aliases=["SR"])
async def sr(ctx):
        ''' Prints out the player's saved SR values.
        '''
        try:
                sender = str(ctx.message.author)
                sr = printPlayerData(sender)
                await ctx.send(sr)
        except:
                await ctx.send("Error 404: SR doesn't exist", delete_after=25)


@client.command()
async def status(ctx):
        ''' Prints what the sender is queued for.
        '''
        # await ctx.message.delete()
        sender = str(ctx.message.author)
        status = printQueueData(sender)
        await ctx.send(ctx.message.author.mention + status, delete_after=25)


##@client.command(aliases=["allsr"])
##async def allSR(ctx):
##        ''' Prints out all the saved SR data.
##        '''
##        try:
##                sr = printAllPlayerData()
##                await ctx.send(sr)
##        except:
##                await ctx.send("Error 404: SR doesn't exist")
       

@client.command()
async def clear(ctx, amount=5):
        ''' Removes a specified amount of messages.
        '''
        # await ctx.message.delete()
        if amount > 0:
                await ctx.channel.purge(limit=amount)


@client.command(aliases=["flip"])
async def coin(ctx):
        ''' Flips a coin.
        '''
        result = random.randint(0,1)
        if result == 0:
                await ctx.send("Heads!")
        else:
                await ctx.send("Tails!")


client.run("token")
