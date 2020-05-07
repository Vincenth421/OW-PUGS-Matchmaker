import discord
from discord.ext import commands

client = commands.Bot(command_prefix = "!")


@client.event
async def on_ready():
	print("Bot is ready")
	
@client.event
async def on_message(message):
    channel = message.channel
    if message.content.startswith("!mention"):
        await client.send_message(channel, message.author.mention)
    
@client.command()
async def test():
        await client.say("hello world!")
        print("test")


@client.command()
async def matchmake():
    pass






client.run("NzA3NzI0OTUzMzUyNTM2MTU2.XrM-yg.Nf4Iwm_kyRuKujCOh1BBqcR8sOM")
