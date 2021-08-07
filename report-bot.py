# this file has some uncommitted changes that I think should be potentially
# kept (such as total_rows), but I'd need to test them to make sure they are
# working first



# Access github : https://github.com/youmslinky/report-bot
# Doug was here
import discord
from discord.ext import commands

import asyncio
import time
import datetime
import random
from datetime import datetime as dt

import sqlite3
import validators
import json

import imgur

EGGPLANT_EMOJI = "🍆"
HEARTS_EMOJI = "💕"
KNIFE_EMOJI = "🔪"
emoji_dic = {
        EGGPLANT_EMOJI:"fucked",
        HEARTS_EMOJI:"married",
        KNIFE_EMOJI:"killed"
        }

DATABASE_NAME = "bot.db"
CONFIG_FILE_NAME = 'config.json'
ALLOWED_ROLES = [
454966304864993281]
#bot commander 454966304864993281

class picture_table_interface():
    #class should have: table_name, database connection, cursor
    def __init__(self,table_name,database_connection,database_cursor,isNSFW):
        self.table_name = table_name
        self.database_connection = database_connection
        self.database_cursor = database_cursor
        self.isNSFW = isNSFW

    def is_nsfw(self):
        return self.isNSFW

    #def nsfw_check_decorator(func):
    #    async def wrapper(self,*args,**kwargs):
    #        if isinstance(ctx.channel, discord.abc.PrivateChannel):
    #            #this is a private channel, we don't need to check
    #            await function(args,ctx)
    #            return
    #        return
    #        if self.is_nsfw:
    #            await func(self,*args,**kwargs)
    #        else:
    #            await

    async def check_if_nsfw(self,args,ctx,function):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            #this is a private channel, we don't need to check
            await function(args,ctx)
            return
        if self.is_nsfw() and not ctx.channel.is_nsfw():
            await ctx.send("This command can only be used in a NSFW channel.")
        else:
            await function(args,ctx)

    def update_image_stats(self,image_id):
        self.database_cursor.execute("UPDATE {} SET viewnumber = viewnumber + 1, unixTimeLastViewed = ? WHERE id = ?".format(self.table_name),(int(round(time.time())),image_id) )
        self.database_connection.commit()

    async def post_random_link(self,args,ctx):
        #reference for fields in database
        #c.execute('CREATE TABLE IF NOT EXISTS hentai(id INTEGER PRIMARY KEY, link TEXT, contributor TEXT, unixTimeAdded INTEGER, unixTimeLastViewed INTEGER, viewNumber INTEGER)')
        self.database_cursor.execute("SELECT * FROM {0} WHERE RANDOM()<(SELECT ((1/COUNT(*))*10) FROM {0}) ORDER BY RANDOM() LIMIT 1".format(self.table_name))
        for row in self.database_cursor:
            if(row['contributor'] == None):
                name = "someone"
            else:
                name = str(row['contributor'])
            msg = await ctx.send("{}\nCourtesy of: {}\nimage id: {}".format(row['link'], name, row['id']) )
            self.update_image_stats(row['id'])
        return msg,row['id']

    async def post_least_seen(self,args,ctx):
        self.database_cursor.execute("SELECT * FROM {} ORDER BY viewNumber LIMIT 1".format(self.table_name))
        for row in self.database_cursor:
                if(row['contributor'] == None):
                    name = "someone"
                else:
                    name = str(row['contributor'])
                await ctx.send("{}\nCourtesy of: {}\nimage id: {}".format(row['link'], name, row['id']) )
                self.update_image_stats(row['id'])

    async def add_links(self,args,ctx):
        #adds links, can add multiple links seperated by spaces
        async with ctx.channel.typing():
            for link in args[1:]:
                if validators.url(link):
                    time_now = int(round(time.time()))
                    respJson = await imgur.image_upload(imageData=link,clientID=config['imgurClientID'])
                    await imgur.add_to_album(imageDeleteHashes=[respJson['data']['deletehash']],albumDeleteHash=self.albumDeleteHash,clientID=config['imgurClientID'])
                    self.database_cursor.execute("INSERT INTO {} (deleteHash,link,originalLink,contributor,unixTimeAdded,viewNumber,unixTimeLastViewed,fucked,married,killed) VALUES (?,?,?,?,?,?,?,?,?,?)".format(self.table_name),
                                              (respJson['data']['deletehash'],respJson['data']['link'],args[1], str(ctx.message.author), time_now, 0, time_now, 0, 0, 0))
                    #self.database_cursor.execute(f"UPDATE {self.table_name} SET deleteHash='{respJson['data']['deletehash']}' WHERE id={int(pic_id)}")
                    self.database_cursor.execute("select id from {} order by unixtimelastviewed desc limit 1".format(self.table_name))
                    for row in self.database_cursor:
                        await ctx.send("Submission added. link id: {}".format(row['id']))
                else:
                    await ctx.send("invalid link")
            self.database_connection.commit()

    async def rm_links(self,args,ctx):
        if await user_has_permission(ALLOWED_ROLES,ctx):
            for pic_id in args[1:]:
                self.database_cursor.execute("DELETE FROM {} WHERE id=?".format(self.table_name),(int(pic_id),))
                if self.database_cursor.rowcount == 1:
                    await ctx.send("{} removed".format(pic_id))
                else:
                    await ctx.send("{} doesn't exist".format(pic_id))
            self.database_connection.commit()
            return
        return

    async def view_link(self,args,ctx):
        for pic_id in args:
            self.database_cursor.execute("SELECT COUNT(*) FROM {} WHERE id=?".format(self.table_name),(int(pic_id),) )
            for row in self.database_cursor:
                rowcount = row['count(*)']
            if rowcount == 1:
                self.database_cursor.execute("SELECT * FROM {} WHERE id=?".format(self.table_name),(int(pic_id),) )
                for row in self.database_cursor:
                    if(row['contributor'] == None):
                        name = "someone"
                    else:
                        name = str(row['contributor'])

                    await ctx.send("{}\nCourtesy of: {}\nimage id: {}".format(row['link'], name, row['id']) )
                    self.update_image_stats(row['id'])
            else:
                await ctx.send("id: {} doesn't exist".format(pic_id))
        return

    async def total_rows(self,args,ctx):
        if len(args) == 1:
            self.database_cursor.execute("select count(rowid) from {}".format(self.table_name))
            for row in self.database_cursor:
                await ctx.send("Total links: {}".format(row['count(rowid)']))
        if len(args) >= 2:
            userCount = 0
            totalCount = 0
            self.database_cursor.execute("select count(rowid) from {} where contributor like ?".format(self.table_name),('%'+args[1]+'%',))
            for row in self.database_cursor:
                userCount = row['count(rowid)']
            self.database_cursor.execute("select count(rowid) from {}".format(self.table_name))
            for row in self.database_cursor:
                totalCount = row['count(rowid)']
            percent = (float(userCount)/totalCount)*100
            await ctx.send(f"total links by {args[1]}: {userCount}/{totalCount} ({percent:.2f}%)")


    async def fmk(self,args,ctx):
        #self.database_cursor.execute(f"insert into fmk(userID, fmkType, fmkDateTime) values(2,'f',datetime('now'))",(,))
        if(self.add_user(args,ctx)==1):
            await ctx.send("You were added to the list of users " + ctx.message.author.mention)
        #adds reactions to a message and then waits for a user to add another then adds the result to the database
        msg,image_id = await self.post_random_link(args,ctx)
        await msg.add_reaction(EGGPLANT_EMOJI)
        await msg.add_reaction(HEARTS_EMOJI)
        await msg.add_reaction(KNIFE_EMOJI)

        def check(reaction, user):
            return reaction.message.id == msg.id and user == ctx.message.author
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            for emoji,_ in emoji_dic.items():
                await msg.remove_reaction(emoji,msg.author)
        else:
            for emoji,_ in emoji_dic.items():
                if emoji != reaction.emoji:
                    await msg.remove_reaction(emoji,msg.author)
            self.database_cursor.execute("UPDATE {0} SET {1} = {1} + 1 WHERE id = {2}".format(self.table_name,emoji_dic[reaction.emoji],int(image_id)))
            self.database_connection.commit()

    async def rehost(self,args,ctx):
        async with ctx.channel.typing():
            for pic_id in args[1:]:
                self.database_cursor.execute("SELECT COUNT(*) FROM {} WHERE id=?".format(self.table_name),(int(pic_id),) )
                for row in self.database_cursor:
                    rowcount = row['count(*)']
                if rowcount == 1:
                    self.database_cursor.execute("SELECT * FROM {} WHERE id=?".format(self.table_name),(int(pic_id),) )
                    respJson = json.dumps({})
                    for row in self.database_cursor:
                        if(row['deleteHash'] is not None):
                            await ctx.send("this image has been rehosted already")
                            return
                        respJson = await imgur.image_upload(imageData=row['link'],clientID=config['imgurClientID'])
                    self.database_cursor.execute(f"UPDATE {self.table_name} SET originalLink=link WHERE id={int(pic_id)}")
                    self.database_cursor.execute(f"UPDATE {self.table_name} SET link='{respJson['data']['link']}' WHERE id={int(pic_id)}")
                    self.database_cursor.execute(f"UPDATE {self.table_name} SET deleteHash='{respJson['data']['deletehash']}' WHERE id={int(pic_id)}")
                    self.database_connection.commit()
                    await imgur.add_to_album(imageDeleteHashes=[respJson['data']['deletehash']],albumDeleteHash=self.albumDeleteHash,clientID=config['imgurClientID'])
                    await ctx.send(f"reshosted at: {respJson['data']['link']}")
                else:
                    await ctx.send("id: {} doesn't exist".format(pic_id))

    async def change_link(self,args,ctx):
        if len(args) != 3:
            await ctx.send("This command requires 2 arguments ex: .w 42 http://example.link")
            return
        pic_id = args[1]
        self.database_cursor.execute(f"UPDATE {self.table_name} SET deleteHash=null WHERE id={int(pic_id)}")
        self.database_cursor.execute(f"UPDATE {self.table_name} SET originalLink=link WHERE id={int(pic_id)}")
        self.database_cursor.execute(f"UPDATE {self.table_name} SET link='{args[2]}' WHERE id={int(pic_id)}")
        self.database_connection.commit()
        await ctx.send(f"id {pic_id} link changed")

    def add_user(self,args,ctx):
        self.database_cursor.execute(f"SELECT COUNT(1) FROM users WHERE discordUserName=?",(str(ctx.message.author),) )
        rowcount = 1
        for row in self.database_cursor:
            rowcount = row['count(1)']
        if rowcount == 0:
            self.database_cursor.execute(f"INSERT INTO users(discordUserName) VALUES(?)",(str(ctx.message.author),) )
            self.database_connection.commit()
            return 1
        else:
            return 0


    async def handle_command(self,args,ctx):
        if len(args)== 0:
            await self.check_if_nsfw(args,ctx,self.post_random_link)
        elif args[0] == 'add':
            await self.add_links(args,ctx)
        elif args[0] == 'rm':
            await self.rm_links(args,ctx)
        elif args[0].isdigit():
            await self.check_if_nsfw(args,ctx,self.view_link)
        elif args[0] == 'total':
            await self.total_rows(args,ctx)
        elif args[0] in {'fmk','f','m','k'}:
            await self.check_if_nsfw(args,ctx,self.fmk)
        elif args[0] == "rehost":
            await self.check_if_nsfw(args,ctx,self.rehost)
        elif args[0] == "relink":
            await self.check_if_nsfw(args,ctx,self.change_link)
        elif args[0] == "addme":
            await self.add_user(args,ctx)
        else:
            await ctx.send(f"unkown option: {args[0]}")



async def user_has_permission(allowed_roles,ctx):
    try:
        #print(ctx.message.author.roles)
        for role in ctx.message.author.roles:
            #print(role,role.id)
            if role.id in allowed_roles:
                return True
        await ctx.send("{} does not have permission to do that".format(ctx.message.author))
        return False
    except:
        await ctx.send("there are no roles here")
        return False




conn = sqlite3.connect(DATABASE_NAME)
conn.row_factory = sqlite3.Row
c = conn.cursor()

waifus = picture_table_interface(table_name='waifus',database_connection=conn,database_cursor=c,isNSFW=False)#,albumDeleteHash=config['waifus']['album']['deleteHash'])
hentai = picture_table_interface(table_name='hentai',database_connection=conn,database_cursor=c,isNSFW=True)#,albumDeleteHash=config['hentai']['album']['deleteHash'])

def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS hentai(id INTEGER PRIMARY KEY, link TEXT, contributor TEXT, unixTimeAdded INTEGER, unixTimeLastViewed INTEGER, viewNumber INTEGER, fucked INTEGER, married INTEGER, killed INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS waifus(id INTEGER PRIMARY KEY, link TEXT, contributor TEXT, unixTimeAdded INTEGER, unixTimeLastViewed INTEGER, viewNumber INTEGER, fucked INTEGER, married INTEGER, killed INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY, discordUserName TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS fmk(fmkID INTEGER PRIMARY KEY, userID INTEGER, fmkType TEXT, fmkDateTime DATETIME)')
    conn.commit()

BOT_PREFIX = ","
#Client = discord.Client()
#client = commands.Bot (command_prefix = ".") # need this for @client.event's to work.
#client = Bot(command_prefix=BOT_PREFIX)
bot = commands.Bot(command_prefix=BOT_PREFIX,activity=discord.Game("with other lolis"))


@bot.event
async def on_ready():
    print('Logged in as') #prints in console
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print ("Bot is ready after {:0.2f} second startup".format(time.time()-time_start))
    #await bot.send_message(bot.get_channel("452904606532632576"), "Bot is ready after {:0.2f} second startup".format(time.time()-time_start))

# Write what you want here.
# To do list -----
# Finish report/reprot command
# Add command that directs people (or just admins) to the source code or seomthing
# Maybe add code for setting reminders in discord (ie .remind 1730 norms, and return a ping to user at 5:30 pm with message "@....norms".)
# hentai linking (lolis prefered) we dont really have any lolis in there.
# Anime suggestion, either draw form site or from list

@bot.command(name='8ball',
                description="answers a yes/no question",
                brief="Answers from the beyond.",
                aliases=['eight_ball','eightball','8-ball'],
                )
async def eight_ball(ctx):
    async with ctx.channel.typing():
        await asyncio.sleep(1,4)
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
        await ctx.send(random.choice(possible_responses) + ", " + ctx.message.author.mention)

@bot.command(name="summon",
                description='summons things',
                brief='summon things',
                #aliases=["bob summoner"],
                )
async def summon(ctx, *args):
    if len(args) == 0:
        print("summon bob or nep or jeremy")
        await ctx.send(str(ctx.message.author.mention) + "summon bob or nep or jeremy")
    elif args[0].lower() == 'bob':
        await ctx.send(str(ctx.message.author.mention) + ", http://i.imgur.com/MYSvmmi.jpg")
    elif args[0].upper() == 'NEP':
        await ctx.send(str(ctx.message.author.mention) + ", https://cdn.discordapp.com/attachments/412847694583824384/454852900624269313/Nep.jpg")
    elif args[0].lower() == 'jeremy':
        await ctx.send(str(ctx.message.author.mention) + ", https://cdn.discordapp.com/attachments/452904606532632576/454849438104551424/IMG_0844.JPG")
    elif args[0].lower() == 'detain':
        await ctx.send(str(ctx.message.author.mention) + ", https://cdn.discordapp.com/attachments/452904606532632576/454946797048299521/SAotUxP.gif")

@bot.command(name='hentai',
                description="Actually hentai, only allowed in nsfw channels", #great description guys
                brief="quenches all your desires",
                aliases=["h", "H"],
                )
async def hentai_pics(ctx,*args):
    await hentai.handle_command(args,ctx)
    return


# I tried to put the questionable stuff towards the top of the list for easier sorting later
@bot.command(name='waifu',
                description="actually waifus",
                brief="quenches all your desires for realsies",
                aliases=["w", "W", "waifus", "Waifus"],
                )
async def waifu(ctx,*args):
    await waifus.handle_command(args,ctx)

async def get_last_pic_id(ctx):
    id = None #id of the latest pic that was posted after a .w or .h
    prevMessage = None #for keeping track of previous message in for loop
    userMessage = None #what command was run to post the pic link .w,.h,etc.
    async for message in ctx.history(limit=10):
        if ctx.message.author == message.author and ".w" in message.content:
            if "image id:" in prevMessage.content:
                id = prevMessage.content.split()[-1]
                userMessage = message
                break
            #print("Author: {}\n{}".format(str(message.author),message.content))
        prevMessage = message
    return id,userMessage

# Add code for dice rolls of different sizes
@bot.command(name='roll',
                description="Uses random function to generate a number from 1 to n using RNG",
                brief="rolls an n sided die",
                )
async def roll(ctx,*args):
    if len(args)== 0: #is this the same as null?
        await ctx.send("usage: .roll n \n(where n is a natural number)")
        return
    try:
        await ctx.send(str(random.randint(1, int(args[0]))))
        return
    except:
        await ctx.send("invalid input\nusage: .roll n\n(where n is a natural number)")

# Report people, count reports individually and collectively, then print out values
@bot.command(name='report',
                description="reports kids only",
                brief="reprot peeps yo",
                aliases=["reprot"]
                )
async def report():
    file_pointer = open('report_count','r+')
    possible_responses = file_pointer.readlines()
    #update and/or create variable
    file_pointer.close()
    await ctx.send(" has been reported.")

#https://github.com/Rapptz/discord.py/blob/async/examples/basic_bot.py
@bot.command(name = "choose",
                description = "picks choices out from a list of choices",
                aliases=["pick","choice"]
                )
async def choose(ctx,*choices : str):
    await ctx.send(random.choice(choices))

# Direct link to c9 ide
@bot.command(name='access',
                description="Access ide",
                )
async def access(ctx):
    await ctx.send(str(ctx.message.author.mention) + ", https://ide.cs50.io/dchuck/ide50")


@bot.command(name='uptime',
                description="amount of time bot has been running",
                brief="bot uptime",
                aliases=["up"]
                )
async def uptime(ctx):
    await ctx.send("up for {}".format(datetime.timedelta(seconds=int(time.time()-time_start))))

# posts link to github for project
@bot.command(name='github',
                description="posts github link",
                )
async def github(ctx):
    await ctx.send(str(ctx.message.author.mention) + ", https://github.com/youmslinky/report-bot")

#uploads database directly to discord with timestamped file
@bot.command(name='database',
                description="Uploads copy of database onto discord",
                aliases=["db"],
                )
async def database_download(ctx,*args):
    await ctx.send("uploading database...")
    timeStamp = dt.isoformat(dt.utcnow().replace(microsecond=0))
    fileName = "{}_{}.db".format(DATABASE_NAME.split('.')[0],timeStamp)
    #fp is the file pointer, filename is what will be displayed in discord
    fileToSend = discord.File(fp=DATABASE_NAME,filename=fileName)
    await ctx.send(file=fileToSend)

def load_config():
    try:
        with open(CONFIG_FILE_NAME,'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError as err:
        #print(err.args)
        raise FileNotFoundError('You need a file named "config.json" with an appropriate discord key to run this bot')
        #print('You need a file named "config.json" with an appropriate discord key to run this bot')

#start main program
time_start = time.time()
try:
    config = load_config()
    hentai.albumDeleteHash = config['hentai']['album']['deleteHash']
    waifus.albumDeleteHash = config['waifus']['album']['deleteHash']
    create_tables()
    bot.run (config['discordClientID'])
except:
    #await bot.close()
    print('failed')

