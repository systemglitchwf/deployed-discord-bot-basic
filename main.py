'''A basic discord bot that can respond to commands and events. in summary of the set up processm, or google it again 

pre set up 

need the pip install command 
python from microsoft store
pip install -U discord.py 
a main area for the code, token space (.env), and requirements.txt

code set up 

in requirements.txt 
discord.py
python-dotenv

in .env
DISCORD_TOKEN=your_token_here
'''

#all this the first 11 lines is just set up fpr this 
import discord 
from discord.ext import commands
import logging
from dotenv import load_dotenv  
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# this is the part where it the what it can do in discord 
intents = discord.Intents.default()
intents.message_content = True 
intents.members = True

# all permisions are int the above intents need to be on discord and the code side of things 

# the ! can be changed to anything  but it signials to the bot that this is a command
bot = commands.Bot(command_prefix='!', intents=intents)

#storage space for role stuff
role_type = "Member"

# this part below is fo rthe handeling of events or ! commands 
@bot.event 
async def on_ready ():
    print(f"the system are functioing at full power, {bot.user.name}")



# this is for whne some one joins the server
@bot.event 
async def on_member_join(member):
    await member.send(f"welcome to the server! {member.name}") 

#this is for checking messages and not auto self replying loop 
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"watch your language {message.author.mention}!")
        # if you have a .author . mention it will ping the user
    await bot.process_commands(message)
    #need this to handle all messages at the end of the on message event


# this is for custom commands
@bot.command() # !hello command
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.mention}!")

# need the role to exist prior to using this command
@bot.command() # !assign command
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=role_type) #must be exact name of the role
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"Assigned {role.name} role to {ctx.author.mention}.")
    else:
        await ctx.send("Role not found.")
# need to be in way of the role to remove the role is !remove NAME_OF_ROLE
@bot.command() # !remove command
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=role_type)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"Removed {role.name} role from {ctx.author.mention}.")
    else:
        await ctx.send("Role not found.")

# commands for role restricted access
@bot.command()

@commands.has_role(role_type) # for role restricted access
async def secret(ctx):
    await ctx.send(f"This is a secret message for {role_type} members only, {ctx.author.mention}!")

@secret.error # error handling for role restricted access
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
            await ctx.send("you dont have permision to use this power")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)