import asyncio
import os
from xmlrpc.client import DateTime
import discord
from discord.ext import commands
from datetime import date, datetime, timedelta
import time


#----------------------------------------------------------------------------------------------------------------------------------------#

bot = commands.Bot(command_prefix='>',help_command=None)

#homework object
workList = []




#event section
@bot.command(name='work', help='show all work')
async def showWork(ctx):
    
    showlist = '\n'.join(workList)
    work_embed = discord.Embed(title="All work", description=showlist, color=0x597DFF)

    await ctx.send(embed=work_embed)

@bot.command(name='add', help='add work (format:>add subject work_name due_date)')
async def addWork(ctx, subject, name, due_date):
    
    #check date format
    check = True
    try:
        check = bool(datetime.strptime(due_date, '%d/%m/%Y'))
    except ValueError:
        check = False

    if check == False:
        await ctx.send("Invalid format Ah-ah")
        return

    #add work to list
    workList.append("due date " + due_date + " - " + subject + " : " + name)

    #set remind date
    due_date2 = datetime.strptime(due_date, '%d/%m/%Y') 
    remind_date = due_date2 - timedelta(days=1)

    #sleep
    waittime = remind_date - datetime.now()
    if(waittime < timedelta(seconds=0)):
        remind_embed = discord.Embed(title="Eh!! " + subject + " homework due tomorrow!!!!", description=name +" due "+ due_date2.strftime('%d/%m/%Y'), color=0xFF5733)
        remind_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=remind_embed)
        return
    await ctx.send("Ok remind " + name + " in " + remind_date.strftime('%d/%m/%Y'))
    await asyncio.sleep(waittime.total_seconds()) 

    #delete work from list
    if datetime.now() == due_date2:
        workList.remove("due date " + due_date + " - " + subject + " : " + name)

    #send remind
    remind_embed = discord.Embed(title=subject + " homework due tomorrow!", description=name +" due "+ due_date2.strftime('%d/%m/%Y'), color=0x4CFC63)
    remind_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=remind_embed)

@bot.command(name='remove', help='remove work (format:>remove subject work_name due_date)')
async def removeWork(ctx, subject, name, due_date):
    
    workList.remove("due date " + due_date + " - " + subject + " : " + name)
    work_embed = discord.Embed(title="Removed!", description="Remove " + subject + " : " + name +" ,Bye BYE!", color=0xC6900)

    await ctx.send(embed=work_embed)

@bot.command(name='clear', help='clear all work (use with caution)')
async def removeWork(ctx):
    
    workList.clear()
    work_embed = discord.Embed(title="All work clear!", description="All work go BYE BYE", color=0xFF0000)

    await ctx.send(embed=work_embed)

@bot.command(name='help', help='clear all work (use with caution)')
async def helpMe(ctx):
    
    help_embed = discord.Embed(title="Help send!", color=0xFF66E0)
    help_embed.add_field(name="Add work", value="use this to add work! >add [Subject] [Work Name] [Due Date(dd/mm/yy)]", inline=False)
    help_embed.add_field(name="Remove work", value="use this to remove work! >remove [Subject] [Work Name] [Due Date(dd/mm/yy)]", inline=False)
    help_embed.add_field(name="Show work", value="use this to show all work! >work", inline=False)
    help_embed.add_field(name="Clear all work", value="use this to clear all work! >clear (use with caution!)", inline=False)

    await ctx.send(embed=help_embed)

bot.run('#notgonnatellya#')