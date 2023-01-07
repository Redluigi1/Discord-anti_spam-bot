from discord.ext import tasks
import discord
from discord.ext import commands 
import re
TOKEN = ''
bot = commands.Bot(command_prefix ='!',intents = discord.Intents.all())
frequencydict = {}                  #this dictionary will maintain the frequency of messages sent by people to prevent spam
regex = {}                          #this dictionary has all the regex 
message_log ={}                     #this dictionary maintains the log of all  messsages sent; gets reset after every 24 hours
badenglist = []                     
with open('eng.csv') as d:
    for x in d:
        badenglist.append(x.strip())
        
        
def badengword(x):
    s = 0
    for z in x.split():
        if z.lower() in badenglist:
            s+=1
        if x.lower() in badenglist:
            s+=1
    if s == 0:
        return 0
    else:
        return 1
        
        
badhinlist = []
with open('hin.csv') as d:
    for x in d:
        badhinlist.append(x.strip())
        
        
def badhinword(x):
    s = 0
    for z in x.split():
        if z.lower() in badhinlist:
            s+=1
        if x.lower in badhinlist:
            s+=1
    if s == 0:
        return 0
    else:
        return 1
    


        

@bot.event
async def on_ready():
    printer.start()
    fun.start()
    print('online')
    
    
    

    
@bot.command()
async def add_regex(ctx,arg1,arg2):
    regex[len(regex)] = [arg1,arg2]                        # arg1 = security level(1,2 or 3); arg2 = regex string 
    
@bot.command()
async def print_regex(ctx):
    await ctx.send(regex)                                   # to print all the regex checks as a key value pair dictionary    
    
@bot.command()
async def remove_regex(ctx,arg):
    try:
        del regex[int(arg)]                                 # to remove a particular regex check; arg is the key of the regex check
    except:
        pass
    
@bot.command()
async def pattern_regex(ctx,arg):
    for x in message_log:                                   # if the bot is unable to stop the spam attack, this can be used to remove all messages of last day satisfying a particular regex check
        if bool(re.search(arg,message_log[x])):
            msg = await ctx.channel.fetch_message(x)
            
            await msg.delete()
            
        




    
@bot.event
async def on_message(message):  
    if message.author != bot.user:
        if badengword(message.content) == 1 or badhinword(message.content) == 1:
            await message.delete()
            
            
            
        for z in regex:
            if regex[z][0] == 1 or '1':           #if security level is 1, the message is silently deleted
                await message.delete()             
            elif regex[z][0] == 2 or '2':           #if security level is 2, the op gets a warning
                await message.delete()
                await message.author.send('This is a warning. Please do not spam the coding club server')
            elif regex[z][0] == 3 or '3':
                await message.delete()            #if security level is 3, op gets kicked out
                try:
                    await bot.kick(message.author)
                except:
                    pass
            else:
                pass
                    
                

        if message.author not in frequencydict:
                frequencydict[message.author] = 1
        else:
                frequencydict[message.author]+=1
                
                
        

        message_log[message.id] = message.content
    
    
@tasks.loop(seconds= 60)
async def printer():
    for x in frequencydict:
        if frequencydict[x] > 50:
            try:
                await bot.kick(x)         #if anyone sends more than 50 messages in 1 minute, he gets kicked out
            except:
                pass
    frequencydict.clear()                   # the frequency dictionary is resetted after every 1 minute


@tasks.loop(hours = 24)
async def fun():
    message_log.clear()                     #this resets the log after every 24 hours
    
      
        
        
   
        
    
bot.run(TOKEN)
