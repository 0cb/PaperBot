#===========================================================================#
#=									   =#
#   Filename:	    PaperBot.py
#   Version:	    2.0
#=									   =#
#   Description:    do it for the lit
#		    - framework ripped ofc, this time from TWO places
#		    - scihub
#                   > use discord rewrite!!!!
#
#=  Author:	    0cb - Christian Bowman				   =#
#   Creation:	    2018-07-01
#   Updated:	    2019-06-09
#=									   =#
#===========================================================================#

#--------------- dependencies ---------------#
#general bot
import discord
import asyncio
#from discord.ext.commands import Bot
from discord.ext import commands
import json

import platform
import csv
import time

#scihub
# it's weird, but you have to have 'scihub.py' within your 'PaperBot' dir
# otherwise, it can't locate the 'SciHub()' function
from scihub import SciHub

#--------------- bot ---------------#

# Here you can modify the bot's prefix and description and whether it sends help in direct messages or not.
#client = Bot (description="PaperBot by 0cb#0093", command_prefix=commands.when_mentioned_or('~'), pm_help = False)
client = commands.Bot(command_prefix='~', description="gey")

@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        return
    else:
        print(error)

# Launch event for server/ bot information
@client.event
async def on_ready():
#print('Logged in as {} (ID: {})'.format(client.user.name, client.user.id))# | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
#    	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
#	print('Use this link to invite {}:'.format(client.user.name))
#	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=510016'.format(client.user.id))
        #Perms: Read msg hist; use ext emojis; send msg; attach files; mention @everyone; add rxn
#	print('--------')
	print('Created by 0cb#0093')
#	return await client.change_presence(game=discord.Game(name='moping around')) #This is buggy, let us know if it doesn't work.


# basic call-response cmd
@client.command()
async def ping(ctx):

	await client.say(":ping_pong: Pong!")
	await asyncio.sleep(3)

@client.command(pass_context=True)
async def remind(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="test")
    await client.say(f"PONG {role}")

@client.command()
async def ivolunteer(ctx):
    chosen = message.author
    role = discord.utils.get(ctx.message.server.roles, name="test")
    await client.say(chosen, "will be our next presenter")
    #await client.say("{}, ".format(role.mention), "our next presenter will be ", chosen)

@client.command(pass_context=True)
async def poke(ctx, member: discord.Member):
    await client.send_message(member, 'You have been selected for the next Journal Club pool. Please respond to the #journal-club channel regarding your ability to present')

@client.command(pass_context=True)
async def getuser(ctx):
    role = discord.utils.get(ctx.message.server.roles, name="Journal Club")
    if role is None:
        await client.say('There is no "test" role on this server!')
        return
    empty = True
    for member in ctx.message.server.members:
        if role in member.roles:
            await client.say("{0.name}#{0.discriminator}".format(member))
            empty = False
    if empty:
        await client.say("Nobody has the role {}".format(role.mention))

@client.command(pass_context=True)
async def stat(ctx):
    #await client.request_offline_members(ctx.message.server)
    role = discord.utils.get(ctx.message.server.roles, name="Journal Club")
    before = time.time()
    #nicknames = [m.name for m in ctx.message.server.members] #if role in member.roles)
    for member in ctx.message.server.members:
        nicknames = (member.name for member in ctx.message.server.members if role in member.roles)
#        if role in member.roles:
        with open('temp.csv', mode='w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect='unix')
            for v in nicknames:
                writer.writerow([v])
    after = time.time()
    await client.send_file(ctx.message.author, 'temp.csv', filename='stats.csv',
                           content="Here's the list. Check PM's. Generated in {:.4}ms".format((after-before)*1000))

#--------------- scihub(?) ---------------#

sh = SciHub()

"""@client.command(pass_context=True)
async def fetch(ctx, url):
    result = sh.fetch(url)
    link = result['url']
    await client.send_message(ctx.message.author, "Here is the requested link", link)
"""

#if __name__ == "__main__":

config = json.load(open('config.json'))
client.run(config['token'])
# Thank you for using this and don't forget to star my repo on GitHub! [Repo Link: https://github.com/Habchy/BasicBot]

# The help command is currently set to be not be Direct Messaged.
# If you would like to change that, change "pm_help = False" to "pm_help = True" on line 9.
