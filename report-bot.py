# Access github : https://github.com/youmslinky/report-bot
import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Game

import asyncio
import time
import datetime
import random
import subprocess
from datetime import datetime as dt

import sqlite3
import validators


class picture_table_interface():
    #class should have: table_name, database connection, cursor
    def __init__(self,table_name,database_connection,database_cursor):
        self.table_name = table_name
        self.database_connection = database_connection
        self.database_cursor = database_cursor
    def update_image_stats(self,image_id):
        self.database_cursor.execute("UPDATE {} SET viewnumber = viewnumber + 1, unixTimeLastViewed = ? WHERE id = ?".format(self.table_name),(int(round(time.time())),image_id) )
        self.database_connection.commit()

    async def post_random_link(self):
        #reference for fields in database
        #c.execute('CREATE TABLE IF NOT EXISTS hentai(id INTEGER PRIMARY KEY, link TEXT, contributor TEXT, unixTimeAdded INTEGER, unixTimeLastViewed INTEGER, viewNumber INTEGER)')
        self.database_cursor.execute("SELECT * FROM {0} WHERE RANDOM()<(SELECT ((1/COUNT(*))*10) FROM {0}) ORDER BY RANDOM() LIMIT 1".format(self.table_name))
        for row in self.database_cursor:
                if(row['contributor'] == None):
                    name = "someone"
                else:
                    name = str(row['contributor'])
                await client.say("{}\nCourtesy of: {}\nimage id: {}".format(row['link'], name, row['id']) )
                update_image_stats(row['id'],self.table_name)
        return

    async def add_links(self,args,context):
        #adds links, can add multiple links seperated by spaces
        for link in args[1:]:
            if validators.url(link):
                time_now = int(round(time.time()))
                self.database_cursor.execute("INSERT INTO {} (link,   contributor,                  unixTimeAdded,viewNumber,unixTimeLastViewed) VALUES (?,?,?,?,?)".format(self.table_name),
                                          (args[1], str(context.message.author), time_now,     0,         time_now))
                self.database_cursor.execute("select id from {} order by unixtimelastviewed desc limit 1".format(self.table_name))
                for row in self.database_cursor:
                    await client.say("Submission added. link id: {}".format(row['id']))
            else:
                await client.say("invalid link")
        self.database_connection.commit()
        return

    async def rm_links(self,args,context):
        for role in context.message.author.roles:
                print(role)
        for pic_id in args[1:]:
            self.database_cursor.execute("DELETE FROM {} WHERE id=?".format(self.table_name),(int(pic_id),))
            await client.say("{} removed".format(pic_id))
        self.database_connection.commit()
        return

    async def view_link(self,args,context):
        for pic_id in args:
            self.database_cursor.execute("SELECT * FROM {} WHERE id=?".format(self.table_name),(int(pic_id),))
            for row in self.database_cursor:
                if(row['contributor'] == None):
                    name = "someone"
                else:
                    name = str(row['contributor'])
                await client.say("{}\nCourtesy of: {}\nimage id: {}".format(row['link'], name, row['id']) )
                update_image_stats(row['id'],self.table_name)
        return

    def total_rows(self):
        self.database_cursor.execute("select count(rowid) from {}".format(self.table_name))
        for row in self.database_cursor:
            return row['count(rowid)']




conn = sqlite3.connect('pic_links.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

waifus = picture_table_interface(table_name='waifus',database_connection=conn,database_cursor=c)
hentai = picture_table_interface(table_name='hentai',database_connection=conn,database_cursor=c)

def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS hentai(id INTEGER PRIMARY KEY, link TEXT, contributor TEXT, unixTimeAdded INTEGER, unixTimeLastViewed INTEGER, viewNumber INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS waifus(id INTEGER PRIMARY KEY, link TEXT, contributor TEXT, unixTimeAdded INTEGER, unixTimeLastViewed INTEGER, viewNumber INTEGER)')
    conn.commit()

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

def update_image_stats(image_id,table_name):
    c.execute("UPDATE {} SET viewnumber = viewnumber + 1, unixTimeLastViewed = ? WHERE id = ?".format(table_name),(int(round(time.time())),image_id) )
    conn.commit()

async def post_random_link(table_name):
    #reference for fields in database
    #c.execute('CREATE TABLE IF NOT EXISTS hentai(id INTEGER PRIMARY KEY, link TEXT, contributor TEXT, unixTimeAdded INTEGER, unixTimeLastViewed INTEGER, viewNumber INTEGER)')
    c.execute("SELECT * FROM {0} WHERE RANDOM()<(SELECT ((1/COUNT(*))*10) FROM {0}) ORDER BY RANDOM() LIMIT 1".format(table_name))
    for row in c:
            if(row['contributor'] == None):
                name = "someone"
            else:
                name = str(row['contributor'])
            await client.say("{}\nCourtesy of: {}\nimage id: {}".format(row['link'], name, row['id']) )
            update_image_stats(row['id'],table_name)
    return

async def add_links(args,context,table_name):
    #adds links, can add multiple links seperated by spaces
    for link in args[1:]:
        if validators.url(link):
            time_now = int(round(time.time()))
            c.execute("INSERT INTO {} (link,   contributor,                  unixTimeAdded,viewNumber,unixTimeLastViewed) VALUES (?,?,?,?,?)".format(table_name),
                                      (args[1], str(context.message.author), time_now,     0,         time_now))
            c.execute("select id from {} order by unixtimelastviewed desc limit 1".format(table_name))
            for row in c:
                await client.say("Submission added. link id: {}".format(row['id']))
        else:
            await client.say("invalid link")
    conn.commit()
    return

async def rm_links(args,context,table_name):
    for role in context.message.author.roles:
            print(role)
    for pic_id in args[1:]:
        c.execute("DELETE FROM {} WHERE id=?".format(table_name),(int(pic_id),))
        await client.say("{} removed".format(pic_id))
    conn.commit()
    return

async def view_link(args,context,table_name):
    for pic_id in args:
        c.execute("SELECT * FROM {} WHERE id=?".format(table_name),(int(pic_id),))
        for row in c:
            if(row['contributor'] == None):
                name = "someone"
            else:
                name = str(row['contributor'])
            await client.say("{}\nCourtesy of: {}\nimage id: {}".format(row['link'], name, row['id']) )
            update_image_stats(row['id'],table_name)
    return

def total_rows(table_name):
    c.execute("select count(rowid) from {}".format(table_name))
    for row in c:
        return row['count(rowid)']

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
        'No',
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
    elif args[0].lower() == 'bob':
        await client.say (str(context.message.author.mention) + ", http://i.imgur.com/MYSvmmi.jpg")
    elif args[0].upper() == 'NEP':
        await client.say (str(context.message.author.mention) + ", https://cdn.discordapp.com/attachments/412847694583824384/454852900624269313/Nep.jpg")
    elif args[0].lower() == 'jeremy':
        await client.say (str(context.message.author.mention) + ", https://cdn.discordapp.com/attachments/452904606532632576/454849438104551424/IMG_0844.JPG")
    elif args[0].lower() == 'detain':
        await client.say (str(context.message.author.mention) + ", https://cdn.discordapp.com/attachments/452904606532632576/454946797048299521/SAotUxP.gif")

@client.command(name='hentai',
                description="not actually hentai", #great description guys
                brief="quenches all your desires",
                aliases=["h", "H"],
                pass_context=True
                )
async def hentai_pics(context,*args):
    if len(args)== 0:
        await hentai.post_random_link()
        return
    if args[0] == 'add':
        await hentai.add_links(args,context)
        return
    if args[0] == 'rm':
        await hentai.rm_links(args,context)
        return
    if args[0].isdigit():
        await hentai.view_link(args,context)
        return
    if args[0] == 'total':
        await client.say("Total links: {}".format(hentai.total_rows()))
        return


# I tried to put the questionable stuff towards the top of the list for easier sorting later
@client.command(name='waifu',
                description="actually waifus",
                brief="quenches all your desires for realsies",
                aliases=["w", "W", "waifus", "Waifus"],
                pass_context=True
                )
async def waifu(context,*args):
    if len(args)== 0:
        await waifus.post_random_link()
        return
    if args[0] == 'add':
        await waifus.add_links(args,context)
        return
    if args[0] == 'rm':
        await waifus.rm_links(args,context)
        return
    if args[0].isdigit():
        await waifus.view_link(args,context)
        return
    if args[0] == 'total':
        await client.say("Total links: {}".format(waifus.total_rows()))
        return
    if args[0] == "rules":
        #await client.say ("Rules:\n1. No nips\n2. No peens\n3. Keep it 2D\n4. Doesn't have to be human\n5. Keep yer hands off the small kids; Only big ones are allowed\n6. Keep yer hands above the table\n7. Dear GOD I hope we can all handle undies")
        await client.say ("Rules:\n1. Nothing explicit, Pls keep this SFW\n2. Only waifus\n3. If you have a question, it prolly goes to .h\n4. No real people")
        return
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
                pass_context=True
                )
async def access(context):
    await client.say (str(context.message.author.mention) + ", https://ide.cs50.io/dchuck/ide50")
    #await client.say ("https://ide.cs50.io/dchuck/ide50")


@client.command(name='uptime',
                description="amount of time bot has been running",
                brief="bot uptime",
                aliases=["up"]
                )
async def uptime():
    await client.say("up for {}".format(datetime.timedelta(seconds=int(time.time()-time_start))))

# posts link to github for project
@client.command(name='github',
                description="posts github link",
                pass_context=True
                )
async def github(context):
    await client.say (str(context.message.author.mention) + ", https://github.com/youmslinky/report-bot")

#uploads file to youm server, then posts link it in discord
@client.command(name='database',
                description="gives link to a copy of the database",
                aliases=["db"],
                )
async def database_download(*args):
    await client.say("uploading database...")
    timeStamp = dt.isoformat(dt.utcnow().replace(microsecond=0))
    fileName = "db_backup/pic_links_{}.db".format(timeStamp)
    process = subprocess.Popen("scp -p pic_links.db c9user@angelthump.hopto.org:/var/www/html/{}".format(fileName),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    (output, err) = process.communicate()
    #print(output.decode('UTF-8'))
    if len(args) != 0:
        domain = "192.168.1.55"
    else:
        domain = "angelthump.hopto.org"
    await client.say("http://{}/{}".format(domain,fileName))

time_start = time.time()
create_tables()
client.run ("NDUyNzY0MDUxODMxOTE0NTA4.DfVE6w.s_kdvvyQK3opFjHTsv5sF1s6xo8")
