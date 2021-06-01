import random, discord, asyncio, time
from asyncio.tasks import wait, sleep
from discord.ext import commands, tasks
from discord.ext.commands import bot, Bot
from random import shuffle

#change the file to be relevant
fileContent = open("setup.txt")
BOT_TOKEN = fileContent.readline()[10:]
botOwnerID = int(fileContent.readline()[3:])

ev = {}
miejsca = {}
pplSh = {}
nums = []
k = 0 
t = 0
tskLst = ['podejdź po salę 6',
'podejdź pod salę 16',
'zejdź na dół amfiteatru',
'podejdź pod windę na parterze',
'podejdź pod windę na pierwszym piętrze',
'podejdź pod windę na drugim piętrze',
'podejdź pod salę 114',
'podejdź pod salę 124',
'podejdź pod salę 214',
'podejdź pod salę 224',
'podejdź pod dowolną kostkę',
'pójdź na bieżnię',
'podejdź pod gabinet pielęgniarki',
'podejdź pod szatnię od wf-u',
'podejdź pod swoją szafkę',
'podejdź do sklepiku',
'podejdź do pokoju nauczycielskiego',
'podejdź pod bibliotekę szkolną',
'podejdź pod wejście na boisko na dachu',
'podejdź pod salę informatyczną',
'podejdź pod portiernię'
]

def rand(n):    
    for x in range(0,n+1):
        nums.append(x)
    shuffle(nums)
    return

def start():
    n = len(ppl)
    if(k<n):
        print("Too few places")
        return ev
    else:
        rand(n)
        for i in range(0, n):
            pplSh[i] = ppl[i], nums[i]
        print("-"*10)
        for j in range (0, n+1):
            for i in range (0, n - 2):
                tmp = {}
                if(pplSh[i][1] > pplSh[i+1][1]):
                    tmp[0] = pplSh[i]
                    pplSh[i] = pplSh[i+1]
                    pplSh[i+1] = tmp[0]
                    del tmp[0]
            i = 0
        if(pplSh[n-1][1] > pplSh[0][1]):
            pplSh[n] = pplSh[0]
        for i in range(0, n-1):
            ev[pplSh[i][0]] = pplSh[i+1][0], miejsca["miejsce " + str(i+1)+ ":"]
        ev[pplSh[n-1][0]] = pplSh[0][0], miejsca["miejsce " + str(n)+ ":"]
        print("Function success")
        print("-"*10)
        return(ev)

async def kill(msgAuth):
    global ev
    tmp = ev[msgAuth][0]
    ev[msgAuth] = ev[ev[msgAuth][0]]
    ev.pop(tmp)
    print(f"The list has been changed")
    await tmp.send("Sorry for your loss. Better luck next time!")
    if(len(ev)>=3):
        await msgAuth.send(f'Your new target is: {format(ev[msgAuth][0])} w miejscu {format(ev[msgAuth][1])}')
        print("The killer has been informed about their new target")
    return 0

client = commands.Bot(command_prefix="!", case_insensitive=True)

#when the bot is ready,
@client.event
async def on_ready():
    global t
    print("-"*10)
    print('Bot is ready')
    print("-"*10)
    print("Basic info:")
    print(f"Username: {client.user.name}")
    print(f"Bot owner's ID: {botOwnerID}")
    print(f"Id: {client.user.id}")
    print(f"Number of reloads: {t}")
    print("-"*10)
    t +=1

@client.command(help = "Start the game with a current list")
async def stt(ctx):
    await ctx.message.add_reaction("😎")
    if (miejsca):
        if(ppl):
            await ctx.send("The game will start with a current setup")
            start()
            d = 1
            for y in ev : #range has to be equal to the length of a list
            #pers = format(ev[y][0])
            #print(pers.lstrip("1234567890#"))
            #format(ev[y][0]).lstrip("123456789#")
                await y.send(f'Musisz zabic osobe: {format(ev[y][0])} w miejscu {format(ev[y][1])}')
                print(f"A message has been sent to {d}")
                d += 1
        else:
            await ctx.send("There's a problem:( [people]")
            return
    else:
        await ctx.send("There's a problem:( [places]")
        return

#on command "ppl",
@client.command(help = "Specify players participating")
async def ppl(ctx):
    global ppl
    ppl = []
    await ctx.message.add_reaction("🥺")
    async with ctx.typing():
        if ctx.message.mentions:
            for x in ctx.message.mentions:
                #add a user identifier to the list ppl[]
                ppl.append(x)
            #send a confirmation
            for y in range(0,(len(ppl))): #range has to be equal to the length of a list
                await ctx.send(f'You\'ve been mentioned, {ppl[y]}. ({y+1}/{len(ppl)})')
            start()
            if(ev):
                d = 1
                for y in ev : #range has to be equal to the length of a list
                    await y.send(f'Musisz zabic osobe: {format(ev[y][0])} w miejscu {format(ev[y][1])}')
                    print(f"A message has been sent to the {d}. person")
                    d += 1
            else:
                await ctx.send("Too few places")
            print("-"*10)
        else:
            await ctx.send("No arguments given")
            print("No arguments")
            print("-"*10)
    return

@client.command(help = "Specify a place for the game; one at a time")
async def plc(ctx):
    #take the k variable
    global k
    if(ctx.message.content.lstrip() != "!plc"):
        #add places to the dictionary miejsca
        miejsca["miejsce " + str(k + 1)+ ":"] = ctx.message.content[5:] #musi usunąc prefix (komendy)-resolved
        await ctx.message.add_reaction("🤯")
        print(f'A place has been added by {ctx.message.author}')
        k = k+1
    #change the k value (number of places and the index for other places)
    await ctx.message.delete()
    await ctx.send(f"Ilosc miejsc: {len(miejsca)}")
    return k

#czyszczenie zmiennych
@client.command(help = "Clear the values")
async def clear(ctx):
    if ctx.message.author.id == botOwnerID:
        global pplSh, ev, miejsca, k, nums
        pplSh = {} #funckja, ludzie w kółku
        ev = {} #final list chyba
        miejsca = {} #ditionary of places
        k = 0 #liczba miejsc
        nums = [] #random numbers
        await ctx.send("Cleared") #confirm
        await ctx.message.add_reaction("😐")
    else:
        await ctx.send("Permissions missing 🤨")

@client.command(help = "Show current lists")
async def show(ctx):
    if ctx.message.author.id == botOwnerID:
        await ctx.send(f"Ilość miejsc: {len(miejsca)}\nIlość osób: {len(pplSh)}")
        await ctx.message.author.send(f"List of places: {miejsca}")
        await ctx.message.author.send(f"Lis of people: {pplSh}")
    else:
        await ctx.send(f"Ilość miejsc: {len(miejsca)}\nIlość osób: {len(pplSh)}")
    return

@client.command()
async def purge(message):
    if message.author.id == botOwnerID:
        purgeChannel = client.get_channel(848631696718037032)
        await purgeChannel.purge(limit=1000)
    else:
        await message.send("Permissions missing 🤨")
    return
'''
@client.command() #deafult sets (for debugging)
async def dea(ctx):
    print(ev)
'''
'''
@tasks.loop(hours=24)
async def called_once_a_day():
    message_channel = client.get_channel(848631696718037032)
    if(pplSh):
        for x in ev:
            await x.send(f"Your task is: {random.choice(tskLst)}. You have one hour")
        await message_channel.send("Tasks for today sent")

@called_once_a_day.before_loop
async def before():
    await client.wait_until_ready()
    target_time = '11:35:00'
    current_epoch = time.time()
    # get string of full time and split it
    time_parts = time.ctime().split(' ')
    # replace the time component to your target
    time_parts[3] = target_time
    # convert to epoch
    future_time = time.mktime(time.strptime(' '.join(time_parts)))
    # if not in the future, add a day to make it tomorrow
    diff = future_time - current_epoch
    if diff < 0:
        diff += 86400
    await asyncio.sleep(diff) #if(12:00 > currentHour): 12:00 - currentHour else: 24h -(currentHour - 12:00)
    print("Tasks sent")

called_once_a_day.start()
'''
@client.event
async def on_message(message):
    channel = client.get_channel(848631696718037032)
    dump = client.get_channel(848540045732216862)
    if message.guild is None and message.author != client.user:
        if(message.content == "kill" or message.content == "Kill"):
            if(len(ev) >= 4):
                print(f"{message.author} has killed {ev[message.author][0]}")
                print("-"*10)
                await channel.send(f"It's official: {message.author} has killed {ev[message.author][0]}. You better be careful now!")
                await kill(message.author)
                await channel.send(f"Number of people left: {len(ev)}")
            else:
                print(f"{message.author} has killed {ev[message.author][0]}")
                print("-"*10)
                await channel.send(f"It's official: {message.author} has killed {ev[message.author][0]}. You better be careful now!")
                await kill(message.author)
                print(f"End. Winners:")
                await channel.send(f"It's the end of the game! The only people left are: ")
                for key in ev:
                    print(format(key))
                    await channel.send(format(key))
            print("-"*10)
            await message.add_reaction("🏆")
        else:
            await dump.send(f'{message.author} has sent a following message: {message.content}')
            print(f'{message.author} has sent a following message: {message.content}')
    await client.process_commands(message)

client.run(BOT_TOKEN)
