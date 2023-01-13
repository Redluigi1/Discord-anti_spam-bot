import datetime
from discord.ext import tasks
import discord
from discord.ext import commands 
import re
TOKEN = 'MTA1ODI0NTkzNjc1ODkxOTE2OA.GNfG9a.XrMPYmdGh7Qtkxu-P5CeoKAuGkITFcfwg0ZM28'
bot = commands.Bot(command_prefix ='!',intents = discord.Intents.all())
frequencydict = {}                  #this dictionary will maintain the frequency of messages sent by people to prevent spam
regex = {}                          #this dictionary has all the regex 
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
    async for x in ctx.channel.history(after = datetime.datetime.now() - datetime.timedelta(hours = 24)):                                   # if the bot is unable to stop the spam attack, this can be used to remove all messages of last day satisfying a particular regex check
        if bool(re.search(arg,x.content)):
            msg = await ctx.channel.fetch_message(x.id)
            
            await msg.delete()
            
        




    
@bot.event
async def on_message(message):  
    if message.author != bot.user:
        if badengword(message.content) == 1 or badhinword(message.content) == 1:
            await message.delete()
            
            
            
        for z in regex:
            if bool(re.search(regex[z][1],message.content)):
                
                if regex[z][0] == '3':
                    await message.delete()            #if security level is 3, op gets kicked out
                    try:
                        await bot.kick(message.author)
                    except:
                        pass
                    break
                    
                    
                if regex[z][0] == '2':           #if security level is 2, the op gets a warning
                    await message.author.send('Please do not spam the Coding Club server')
                    await message.delete()
    
                    
                if regex[z][0] == '1':           #if security level is 1, the message is silently deleted
                    await message.delete()             

                    

               
                    
                

        if message.author not in frequencydict:
                frequencydict[message.author] = 1
        else:
                frequencydict[message.author]+=1
                
                
        

       
        
        await bot.process_commands(message)
    
    
@tasks.loop(seconds= 30)
async def printer():
    for x in frequencydict:
        if frequencydict[x] > 25:
            try:
                await bot.kick(x)         #if anyone sends more than 25 messages in 0.5 minutes, he gets kicked out
            except:
                pass
    frequencydict.clear()                   # the frequency dictionary is resetted after every 1 minute


    
    
      
        
    
   
        
    
bot.run(TOKEN)
