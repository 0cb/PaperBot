#===========================================================================#
#=									   =#
#   Filename:	    PaperBot.py
#   Version:	    2.0
#=									   =#
#   Description:    do it for the lit
#                   - framework ripped
#                   - sci-hub
#                   > discord.py 1.2.2
#                   > python 3.5+
#
#=  Author:	    0cb - Christian Bowman				   =#
#   Creation:	    2018-07-01
#   Updated:	    2019-06-20 15:11
#=									   =#
#===========================================================================#

#--------------- notes ---------------#

# with the migration to discord.py 1.2.2, shit's changed, so we have to redo syntax and shit
# ie:
#   bot.say -> ctx.send
#   client.send_ -> channel.send

#--------------- todo ---------------#

# figure out server

#--------------- dependencies ---------------#

import discord
from discord.ext import commands
import json
import platform
import asyncio

import csv
import time
import pandas as pd

from scihub import SciHub

#--------------- bot ---------------#
bot = commands.Bot(command_prefix='~', description="PaperBot by 0cb#0093")

# __(2019-06-14 12:11)__ run on PaperBot startup
@bot.event
async def on_read():
    print('Logged in as ' + bot.user.name + '-' + bot.user.id)


"""    print('Logged in as ') #if you try to do the whole +bot.__+ thing, it messes with the indentations
    print(bot.user.name)
    print(bot.user.id)
    print('----------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('----------')
    print('Ready to cry')
    print('')"""

# __(2019-06-15 20:35)__ help list generated from https://cog-creators.github.io/discord-embed-sandbox/
@bot.command()
async def info(ctx):
    embed=discord.Embed(title="List of commands", description="prefix: ~ ")
    embed.set_author(name="PaperBot")
    embed.add_field(name="ping", value="test command", inline=False)
    embed.add_field(name="ivolunteer", value="volunteer as next presenter", inline=False)
    embed.add_field(name="whovolunteered", value="check who is next presenter", inline=False)
    embed.add_field(name="remind <user>", value="send a gentle reminder to those selected", inline=False)
    embed.add_field(name="stat", value="grab a list of all channel members", inline=False)
    embed.add_field(name="fetch <url>", value="get a link for access to a pay-walled article \n ex. ~fetch https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3531285/", inline=False)
    await ctx.send(embed=embed)

# __(2019-06-14 12:12)__ test command
# use: ~ping
@bot.command()
async def ping(ctx):
    await ctx.send('Welcome to SkyNet :robot:')

# __(2019-06-15 19:32)__ writes message author to file for recall using 'whovolunteered'
# use: ~ivolunteer
# note: writes user's ID rather than username
@bot.command()
async def ivolunteer(ctx):
    await ctx.send(ctx.message.author.mention+' has offered to be the next presenter')
    with open('volunteer.txt', 'a') as file:    # 'a' is for appending vs 'w (write)' or 'r (read)'
        file.write(ctx.message.author.mention + ' volunteered  ' + str(time.asctime()) + '\n')
    print('New volunteer written to list')

# __(2019-06-15 19:33)__ outputs last line of the volunteer list for the channel
# use: ~whovolunteered
#  TODO: if statement to prevent double volunteer <19-06-20, cb> # 
@bot.command()
async def whovolunteered(ctx):
    with open('volunteer.txt') as chosen:
        recent = (list(chosen)[-1])
    await ctx.send(recent)

# __(2019-06-14 12:29)__ sends a PM; works with '@member' and 'member'
# use: ~remind <member>
@bot.command()
async def remind(ctx, member: discord.Member):
    embed=discord.Embed(title="You have been selected for the next #journal-club presentation! Please reply in the r/labrats #journal-club channel using the following template", description='~presenting @Journal Club "(date (whatever day you want))" "(topic url)"')
    #await member.send('You have been selected for the next journal-club presentation. Please reply in the r/labrats #journal-club channel using the following template: \n\n~presenting @Journal Club "(when)" "(topic url)"')
    embed.add_field(name="Here is an example: ", value='~presenting @Journal Club "June 23 (Sunday) at 14:00 PDT" "De novo domestication of wild tomato using genome editing https://www.nature.com/articles/nbt.4272"')
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name="Please read the following notes: ", value='You do NOT have to present- just acknowledge whether you can/ cannot')
    embed.add_field(name='\u200b', value='JC does NOT have to be Sunday- you can make it any day you want, but just keep in mind other members have time-zone differences, so weekends are preferred')
    embed.add_field(name='\u200b', value='I get it, people are busy. JC is a bit of a time commitment, but it is harder to manage JC without communication: no response to 2 reminders, and I might have to remove the JC tag. This can always be readded via ?ranks in bot-commands')
    #await member.send('~presenting @Journal Club "<when>" "<topic & url>"\n Here is an example: \n~presenting @Journal Club "June 23 (Sunday) at 14:00 PDT" "De novo domestication of wild tomato using genome editing https://www.nature.com/articles/nbt.4272"')
    await member.send(embed=embed)

#  __(2019-07-28 03:53)__ sends PM to multiple members
#  use: ~remind2 <member1> <member2>#
@bot.command()
async def remind2(ctx, member1: discord.Member, member2: discord.Member):
    embed=discord.Embed(title="You have been selected for the next #journal-club presentation. Please reply in the r/labrats #journal-club channel using the following template", description='~presenting @Journal Club "(date (whatever day you want))" "(topic url)"')
    #await member.send('You have been selected for the next journal-club presentation. Please reply in the r/labrats #journal-club channel using the following template: \n\n~presenting @Journal Club "(when)" "(topic url)"')
    embed.add_field(name="Here is an example: ", value='~presenting @Journal Club "June 23 (Sunday) at 14:00 PDT" "De novo domestication of wild tomato using genome editing https://www.nature.com/articles/nbt.4272"')
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name="Please read the following notes: ", value='You do NOT have to present- just acknowledge whether you can/ cannot')
    embed.add_field(name='\u200b', value='JC does NOT have to be Sunday- you can make it any day you want, but just keep in mind other members have time-zone differences, so weekends are preferred')
    embed.add_field(name='\u200b', value='I get it, people are busy. JC is a bit of a time commitment, but it is harder to manage JC without communication: no response to 2 reminders, and I might have to remove the JC tag. This can always be readded via ?ranks in bot-commands')
    #await member.send('~presenting @Journal Club "<when>" "<topic & url>"\n Here is an example: \n~presenting @Journal Club "June 23 (Sunday) at 14:00 PDT" "De novo domestication of wild tomato using genome editing https://www.nature.com/articles/nbt.4272"')
    await member1.send(embed=embed)
    await member2.send(embed=embed)

#  __(2019-07-28 03:53)__ sends PM to multiple members
#  use: ~remind3 <member1> <member2> <member3> <member4> <member5>#
@bot.command()
async def remind3(ctx, member1: discord.Member, member2: discord.Member, member3: discord.Member):
    embed=discord.Embed(title="You have been selected for the next #journal-club presentation. Please reply in the r/labrats #journal-club channel using the following template", description='~presenting @Journal Club "(date (whatever day you want))" "(topic url)"')
    #await member.send('You have been selected for the next journal-club presentation. Please reply in the r/labrats #journal-club channel using the following template: \n\n~presenting @Journal Club "(when)" "(topic url)"')
    embed.add_field(name="Here is an example: ", value='~presenting @Journal Club "June 23 (Sunday) at 14:00 PDT" "De novo domestication of wild tomato using genome editing https://www.nature.com/articles/nbt.4272"')
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name="Please read the following notes: ", value='You do NOT have to present- just acknowledge whether you can/ cannot')
    embed.add_field(name='\u200b', value='JC does NOT have to be Sunday- you can make it any day you want, but just keep in mind other members have time-zone differences, so weekends are preferred')
    embed.add_field(name='\u200b', value='I get it, people are busy. JC is a bit of a time commitment, but it is harder to manage JC without communication: no response to 2 reminders, and I might have to remove the JC tag. This can always be readded via ?ranks in bot-commands')
    #await member.send('~presenting @Journal Club "<when>" "<topic & url>"\n Here is an example: \n~presenting @Journal Club "June 23 (Sunday) at 14:00 PDT" "De novo domestication of wild tomato using genome editing https://www.nature.com/articles/nbt.4272"')
    await member1.send(embed=embed)
    await member2.send(embed=embed)
    await member3.send(embed=embed)

#  __(2019-07-28 03:53)__ sends PM to multiple members
#  use: ~remind4 <member1> <member2> <member3> <member4>#
@bot.command()
async def remind4(ctx, member1: discord.Member, member2: discord.Member, member3: discord.Member, member4: discord.Member):
    embed=discord.Embed(title="You have been selected for the next #journal-club presentation. Please reply in the r/labrats #journal-club channel using the following template", description='~presenting @Journal Club "(date (whatever day you want))" "(topic url)"')
    #await member.send('You have been selected for the next journal-club presentation. Please reply in the r/labrats #journal-club channel using the following template: \n\n~presenting @Journal Club "(when)" "(topic url)"')
    embed.add_field(name="Here is an example: ", value='~presenting @Journal Club "June 23 (Sunday) at 14:00 PDT" "De novo domestication of wild tomato using genome editing https://www.nature.com/articles/nbt.4272"')
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name="Please read the following notes: ", value='You do NOT have to present- just acknowledge whether you can/ cannot')
    embed.add_field(name='\u200b', value='JC does NOT have to be Sunday- you can make it any day you want, but just keep in mind other members have time-zone differences, so weekends are preferred')
    embed.add_field(name='\u200b', value='I get it, people are busy. JC is a bit of a time commitment, but it is harder to manage JC without communication: no response to 2 reminders, and I might have to remove the JC tag. This can always be readded via ?ranks in bot-commands')
    #await member.send('~presenting @Journal Club "<when>" "<topic & url>"\n Here is an example: \n~presenting @Journal Club "June 23 (Sunday) at 14:00 PDT" "De novo domestication of wild tomato using genome editing https://www.nature.com/articles/nbt.4272"')
    await member1.send(embed=embed)
    await member2.send(embed=embed)
    await member3.send(embed=embed)
    await member4.send(embed=embed)

#  __(2019-07-28 03:53)__ sends PM to multiple members
#  use: ~remindall <member1> <member2> <member3> <member4> <member5>#
@bot.command()
async def remindall(ctx, member1: discord.Member, member2: discord.Member, member3: discord.Member, member4: discord.Member, member5: discord.Member):
    embed=discord.Embed(title="You have been selected for the next #journal-club presentation. Please reply in the r/labrats #journal-club channel using the following template", description='~presenting @Journal Club "(date (whatever day you want))" "(topic url)"')
    #await member.send('You have been selected for the next journal-club presentation. Please reply in the r/labrats #journal-club channel using the following template: \n\n~presenting @Journal Club "(when)" "(topic url)"')
    embed.add_field(name="Here is an example: ", value='~presenting @Journal Club "June 23 (Sunday) at 14:00 PDT" "De novo domestication of wild tomato using genome editing https://www.nature.com/articles/nbt.4272"')
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name="Please read the following notes: ", value='You do NOT have to present- just acknowledge whether you can/ cannot')
    embed.add_field(name='\u200b', value='JC does NOT have to be Sunday- you can make it any day you want, but just keep in mind other members have time-zone differences, so weekends are preferred')
    embed.add_field(name='\u200b', value='I get it, people are busy. JC is a bit of a time commitment, but it is harder to manage JC without communication: no response to 2 reminders, and I might have to remove the JC tag. This can always be readded via ?ranks in bot-commands')
    #await member.send('~presenting @Journal Club "<when>" "<topic & url>"\n Here is an example: \n~presenting @Journal Club "June 23 (Sunday) at 14:00 PDT" "De novo domestication of wild tomato using genome editing https://www.nature.com/articles/nbt.4272"')
    await member1.send(embed=embed)
    await member2.send(embed=embed)
    await member3.send(embed=embed)
    await member4.send(embed=embed)
    await member5.send(embed=embed)
    #  TODO: draw users for PM from 'selected' list <19-06-15, cb> #

# __(2019-06-20 15:15)__ message template for presentations/ reminders(?)
# use: ~presenting <role> <day and date> <
@bot.command()
async def presenting(ctx, role: discord.Role, when, topic):
    with open('volunteer.txt') as chosen:
        recent = (list(chosen)[-1])
    #role = discord.utils.get(ctx.guild.roles, name="Journal Club")
    #role = discord.utils.get(ctx.guild.roles, name="test")
    #await ctx.send('The next ' + ctx.channel.mention + 'testing 1 2 3 ')
    #await ctx.send('The next ' + ctx.role.mention + 'testing 123')
    await ctx.send(f'The next {role.mention} will be **{when}**\n\n**Presenter:** {recent}**Topic:** {topic}\n\nThe PDF can be found at:\nhttps://drive.google.com/drive/folders/1AZd8RUbn1yotKE-7TTt3aB712owfpH74\nPlease use https://www.timeanddate.com/worldclock/fixedform.html to set the meeting\n\nThrow a :pipetteup: if you can attend!')


#--------------- Main functions ---------------#

# __(2019-06-14 22:15)__ grabs members in channel, sends PM with .csv of said list
# use: ~stat
@bot.command()
async def stat(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Journal Club")
    #role = discord.utils.get(ctx.guild.roles, name="test")

    for member in ctx.guild.members:
        nicknames = (member.name for member in ctx.guild.members if role in member.roles)
        with open('temp.csv', mode='w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar=' ', dialect='unix')
            for v in nicknames:
                writer.writerow([v])
    await ctx.author.send('Here is the list of journal-club members', file=discord.File('temp.csv'))

#  __(2019-07-28 03:08)__ sends output from 'selection' script 
#  use: ~selection
@bot.command()
async def selection(ctx):
    #with open('./Selected.JC/selection.csv') as chosen:
    #    names = chosen.readlines()
    #    for x in names:
    #        print (x)

    await ctx.send("The following members have been selected: ")
    df = pd.read_csv('./Selected.JC/selection.csv')
    await ctx.send(df)

@bot.command()
async def bye(ctx, member: discord.Member):
    embed=discord.Embed(title="You have been removed from the #journal-club for inactivity.", description="If you would like to participate in JC, you are welcome to re-add your role using ?rank Journal Club, but it is too hard to run #journal-club without communication. Sorry!")
    await member.send(embed=embed)

@bot.command()
async def bye4(ctx, member1: discord.Member, member2: discord.Member, member3: discord.Member, member4: discord.Member):
    embed=discord.Embed(title="You have been removed from the #journal-club for inactivity.", description="If you would like to participate in JC, you are welcome to re-add your role using ?rank Journal Club, but it is too hard to run #journal-club without communication. Sorry!")
    await member1.send(embed=embed)
    await member2.send(embed=embed)
    await member3.send(embed=embed)
    await member4.send(embed=embed)

#--------------- sci-hub stuff ---------------#
"""
sh = SciHub()

@bot.command()
async def fetch(ctx, url):
    result = sh.fetch(url)
    link = result['url']
    await ctx.send(link)
    #await ctx.author.send(link)
"""
#  TODO: download pdf and send? <19-06-15, cb> # 

#--------------- EoF ---------------#
#json to hold our token so we don't have skynet2.0

config = json.load(open('config.json'))
bot.run(config['token'])
