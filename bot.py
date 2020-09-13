import random
import discord
import json
from discord.ext import commands
from random import randint


Defualt_bot_prefix = '/' # <== you can change this
token = '' # your token
client = commands.Bot(command_prefix=Defualt_bot_prefix)

#This will tell if the bot is ready or not:
# All events for the bot
@client.event
async def on_ready():
    print("connection has been establish")
    print('We have logged in as {0.user}' .format(client))
'''
# if you want to band any cursed words
@client.event
async def on_message(message):
    words = ['fick', 'shot', 'xxx', 'ddd', 'xxx2'] #dont put admin
    for word in words:
        if message.content.count(word) > 0:
            print("No")
            await message.channel.purge(limit=1)


#this will print out everyones message in the terminal:
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    await client.process_commands(message)
'''

#if someone deleted a message the bot will send this message:
@client.event
async def on_message_delete(message):
    await message.channel.send("Message has been deleted from the server")

#if someone join's the server it will print out this message:
@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

#if someones leave the server it will print out this message:
@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')

#All commands to used:
#sends a message to the user to the server:
@client.command(help='sends a ping request to the server')
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

#send a messages to the user:
@client.command(brief='send you a message to check if the server is online or not')
async def test(ctx):
    await ctx.author.send("Bot is online now")
    print("Message send")

#delets a message from the server:
@client.command(help='cleans the message')
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
    await ctx.channel.send("message has been purge from the server.")

# kick someone from the server:
@client.command(brief='kick someone from the server')
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

# ban command for user:
@client.command(brief='banned someone from the server(admin only)')
@commands.has_permissions(manage_messages=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


# unban command for user:
@client.command(brief='Unbanned someone from the server(admin only)')
@commands.has_permissions(manage_messages=True)
async def unban(ctx, *, member):
    banned_user = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_user:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

# For creating new channels for admin:
@client.command(brief='!create-channel name (admin)',name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='xxx'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

# Tells you some info about the member:
@client.command(brief='checks if a member is there.')
async def info(ctx, *, member: discord.Member):
    fmt = '{0} joined on {0.joined_at} and has {1} roles.'
    await ctx.send(fmt.format(member, len(member.roles)))

#Games to play:
# play 8ball:
@client.command(aliases=['8ball', 'ball'], brief='play 8ball')
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is a decidedly so.',
                 'without a doubt',
                 'yes - definitely',
                 'you may rely on it.',
                 'As I see it yes',
                 'Most likely',
                 'yes',
                 'very doubtful',
                 'My reply is no']

    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


# simulates rolling dice:
@client.command(name='roll dice', brief='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

# this will read the file called cat.txt and send a random cat picture:
@client.command(aliases2=['cat', 'ctp'], brief='sends cat pictures')
async def cat(ctx):
    with open('cat.txt', 'r') as f:
        op = f.readlines()
        await ctx.send(random.choice(op))

#this will send a cat picture from the folder:
@client.command(aliases3=['fol_cat', 'cat_fol'], brief='send a random cat pic from folder')
async def cat_folder(ctx):
    try:
        fol = randint(0,2)
        await ctx.send(str('heres some cat pic\n') ,file=discord.File("cat_pic/{}.jpg".format(fol)))
    except:
        pass


client.run(token)