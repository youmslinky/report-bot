import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Game

import asyncio
import time
import datetime
import random

import validators



BOT_PREFIX = "."
#Client = discord.Client()
#client = commands.Bot (command_prefix = ".") # need this for @client.event's to work.
client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_ready():
    print('Logged in as') #prints in console
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=Game(name="with other bots"))
    print('------')
    print ("Bot is ready after {:0.2f} second startup".format(time.time()-time_start))
    await client.send_message(client.get_channel("452904606532632576"), "Bot is ready after {:0.2f} second startup".format(time.time()-time_start))

# Write what you want here.
# To do list -----
# Finish report/reprot command
# Add command that directs people (or just admins) to the source code or seomthing
# Maybe add code for setting reminders in discord (ie .remind 1730 norms, and return a ping to user at 5:30 pm with message "@....norms".)
# hentai linking (lolis prefered) we dont really have any lolis in there.
# Anime suggestion, either draw form site or from list

# Basic @client.event example:
# @client.event
# async def on_message(message):
#     if message.content == "hello":
#         print(message.channel)
#         type(message.channel)
#         await client.send_message(message.channel, "Hello, World!")

# @client.command()
# async def report(message):
    # if message.content.upper().startswith ("REPORT"):
    #     args = message.content.split (" ")
    #     await client.send_message(message.channel, "%s" % (" ".join(args[1:]) + " has been reported."))
    # if message.content.upper().startswith (".DING"):
    #     userID = message.author.id
    #     await client.send_message (message.channel, "<@%s> Dong!" % (userID))

    # # if message.content.upper().startswith (".HALP"):
    # #     userID = message.author.id
    # #     await client.send_message (message.channel, "<@%s>, use '!' for Rythm bot and '?' for weeb bot. Use '.summon bob' to summon Bob Ross." % (userID))

    # if message.content.upper().startswith ("DOUG"):
    # #if message.content.includes ("doug"):
    #     userID = message.author.id
    #     await client.send_message (message.channel, "<@%s> FUCK YOU" % (userID))


    # if message.content.upper().startswith (".REPORT"):
    #     args = message.content.split (" ")
    #     # .report Hey There
    #         # args[0] = .REPORT
    #         # args[1] = Hey
    #         # args[2] = There
    #         # args[1:] = Hey There
    #     await client.send_message(message.channel, "%s" % (" ".join(args[1:]) + " has been reported."))






@client.command(name='8ball',
                description="answers a yes/no question",
                brief="Answers from the beyond.",
                aliases=['eight_ball','eightball','8-ball'],
                pass_context=True
                )
async def eight_ball(context):
    possible_responses = [
        'Thats gonna be a no from me dawg',
        'It is not looking likely',
        'Hell no',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
        'Yes',
        'No'
        'Mmmmmmmmmmmmmmmmmm no'
        ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

@client.command(name="summon",
                description='summons things',
                brief='summon things',
                #aliases=["bob summoner"],
                pass_context=True
                )
async def summon(context, *args):
    if len(args) == 0:
        print("summon bob or nep or jeremy")
    if args[0].lower() == 'bob':
        await client.say (str(context.message.author.mention) + ", http://i.imgur.com/MYSvmmi.jpg")
    if args[0].upper() == 'NEP':
        await client.say (str(context.message.author.mention) + ", https://cdn.discordapp.com/attachments/412847694583824384/454852900624269313/Nep.jpg")
    if args[0].lower() == 'jeremy':
        await client.say (str(context.message.author.mention) + ", https://cdn.discordapp.com/attachments/452904606532632576/454849438104551424/IMG_0844.JPG")
    if args[0].lower() == 'detain':
        await client.say (str(context.message.author.mention) + ", https://cdn.discordapp.com/attachments/452904606532632576/454946797048299521/SAotUxP.gif")

@client.command(name='hentai',
                description="not actually hentai", #great description guys
                brief="quenches all your desires",
                aliases=["h", "H"],
                pass_context=True
                )
async def hentai(context,*args):
    if len(args)== 0:
        file_pointer = open('hentai_links','r')
        possible_responses = file_pointer.readlines() # Does this skip blank lines?
        file_pointer.close()
        await client.say(random.choice(possible_responses))
        return
    if args[0] == 'add':
        file_pointer = open('hentai_links','a')
        for link in args[1:]:
            if validators.url(link):
                file_pointer.write(args[1])
                #file_pointer.write(","+str(context.message.author)) #uncomment to put user data into log, but will show up in the link
                file_pointer.write('\n')
                await client.say("Submission added.")
            else:
                await client.say("invalid link")
        file_pointer.close()
        #Code for permissions w/ ability to approve those to use command from discord (maybe move disallowed client id's to an allowed id's file?)

# I tried to put the questionable stuff towards the top of the list for easier sorting later
@client.command(name='waifu',
                description="actually waifus",
                brief="quenches all your desires for realsies",
                aliases=["w", "W", "waifus", "Waifus"],
                pass_context=True
                )
async def definitely_hentai(context,*args):
    if len(args)== 0:
        with open('dick_pics') as file_pointer: #used this instead of file_pointer = open('dick_pics','r') and indented next 4 lines.  I don't think this really does much to the code except to create more indents.
            possible_responses = file_pointer.readlines()
            #file_pointer.close() #I think the "with open..." code auto calls that.
            await client.say(random.choice(possible_responses))
            return
    if args[0] == 'add':
        file_pointer = open('dick_pics','a')
        #with open('dick_pics') as file_pointer:
        for link in args[1:]:
            if validators.url(link):
                file_pointer.write(args[1])
                #file_pointer.write("#,"+str(context.message.author)) #uncomment to put user data into log, but will show up in the link
                file_pointer.write('\n')
                await client.say("Waifu submission added.")
            else:
                await client.say("Invalid link")
        file_pointer.close()
    if args[0] == "rules":
        await client.say ("Rules:\n1. No nips\n2. No peens\n3. Keep it 2D\n4. Doesn't have to be human\n5. Keep yer hands off the small kids; Only big ones are allowed\n6. Keep yer hands above the table\n7. Dear GOD I hope we can all handle undies")
        #await client.say ("Rules:\n1. Nothing explicit\n2. Only waifus\n3. Undies are ok (I think?), but no butts poking out of the monitor with a lost piece of clothing in there"\n4. No real people)
    if args[0] == "remove":
        if "454966304864993281" in [role.id for role in context.message.author.roles]:
            # file_pointer = open('dick_pics', 'a')
            # for link in args[1:]:
            #     if validators.url(link):
            #         #file_pointer.remove('dick_pics', args[1])
            #         print (args[1])
            #         await client.say("Link removed")
                with open('dick_pics') as file_pointer:
                    #file_pointer = open('dick_pics', 'r+')
                    for link in args[1:]:
                        #try:
                            if validators.url(link):
                                #file_pointer.list.remove(line.strip () + args[1])
                                #file_pointer.remove("%s" % args[1])
                                file_pointer.remove (args[1])
                                print (args[1])
                                await client.say("Link removed")
                        #except:
                            #await client.say ("Ya, that didn't work")
        else:
            await client.say("You are not worthy") #await client.say("You do not have permission)")


# Add code for dice rolls of different sizes
@client.command(name='roll',
                description="Uses random function to generate a number from 1 to n using RNG",
                brief="rolls an n sided die",
                )
async def roll(*args):
    if len(args)== 0: #is this the same as null?
        await client.say("usage: .roll n \n(where n is an integer)")
        return
    try:
        await client.say(str(random.randint(1, int(args[0]))))
        return
    except:
        await client.say("invalid input\nusage: .roll n\n(where n is an integer)")

# Report people, count reports individually and collectively, then print out values
@client.command(name='report',
                description="reports kids only",
                brief="reprot peeps yo",
                aliases=["reprot"]
                )
async def report():
    file_pointer = open('report_count','r+')
    possible_responses = file_pointer.readlines()
    #update and/or create variable
    file_pointer.close()
    await client.say (" has been reported.")

#https://github.com/Rapptz/discord.py/blob/async/examples/basic_bot.py
@client.command(name = "choose",
                description = "picks choices out from a list of choices"
                )
async def choose(*choices : str):
    await client.say(random.choice(choices))

# Direct link to c9 ide
@client.command(name='access',
                description="Access ide",
                )
async def access():
    await client.say (str(context.message.author.mention) + ", https://ide.cs50.io/dchuck/ide50")
    #await client.say ("https://ide.cs50.io/dchuck/ide50")


@client.command(name='uptime',
                description="amount of time bot has been running",
                brief="bot uptime",
                aliases=["up"]
                )
async def uptime():
    await client.say("up for {}".format(datetime.timedelta(seconds=int(time.time()-time_start))))


time_start = time.time()
client.run ("NDUyNzY0MDUxODMxOTE0NTA4.DfVE6w.s_kdvvyQK3opFjHTsv5sF1s6xo8")