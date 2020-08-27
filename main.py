import discord
from discord.ext import commands
import time
import random
from raceStats import player

TOKEN = ''
client = commands.Bot(command_prefix = '.')
adventurers = {}
finalRole = {}
rolesDes = open("Roles", "r", encoding='utf8')
roleList = ['🧙', '⚔', '🗡', '🧞', '🎸', '🔮', '🛡', '🪓', '☄', '😇', '🌲', '☯', '🏹', '🃏', '🧠']
rolelock = False
readyNum = 0
members = {}

@client.event
async def on_ready():
    print("Campaign has started")
    adventurers.clear()

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.author != client.user: #it will only detect emojis directed at its own message
        return
    if user == client.user:#it wont count itself as an adventurer
        return
    if reaction.emoji == '✅':
        if reaction.count == (len(adventurers) + 1) and len(adventurers) != 0:
            await reaction.message.channel.send("Role Locked, all party members ready to start.\nTo set race as well as stats, please send this message: Character Choice: <name> <level> <race>(or subrace if applicable) <strength> <dexterity> <constitution> <intellect> <wisdom> <charisma>")
            finalRole = adventurers
            print(finalRole)
            return
    if user.name in adventurers:
        return
    adventurers[str(user.name)] = reaction.emoji
    await reaction.message.channel.send(f'{user.name} joined the party as {reaction.emoji}')

@client.event
async def on_reaction_remove(reaction, user):
    if reaction.message.author != client.user:
        return
    if user.name not in adventurers:
        return
    if adventurers[user.name] != reaction.emoji:
        return
        print("adventurer has a different role")
    del adventurers[user.name]
    await reaction.message.channel.send(f'{user.name} was removed from party')

@client.command()
async def ping(ctx):
    await ctx.send('Whomst has awakened the ancient one')

@client.command()
async def charCreate(ctx):
    message = await ctx.send("React to this to choose your role.")
    for emoji in roleList:
        await message.add_reaction(emoji)

    message2 = await ctx.send("React to this to get ready and lock all roles")
    await message2.add_reaction('✅')

@client.command()
async def roles(ctx):
    await ctx.send(rolesDes.read())

@client.command()
async def memberslist(ctx):
    if len(adventurers) == 0:
        await ctx.send("Wow, such an empty party. "
                       "Consider joining by sending .charCreate.")
        return
    await ctx.send("Party members list:")
    for x in adventurers:
        await ctx.send(f"{x} as {adventurers[x]}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.bot:
        return

    await client.process_commands(message)

    content = message.content.lower()
    if "dice" in content:
        contentList = content.split(" ")
        try:
            num = contentList[contentList.index('dice') + 1]
            repeat = contentList[contentList.index('dice') + 2]
        except IndexError:
            await message.channel.send('Syntax is invalid, try again\n'
                                       'Valid syntax would look like: "dice <dice number> <number of rolls>"')

        try:
            for x in range(int(repeat)):
                value = random.randint(1, int(num))
                await message.channel.send(f'Dice Roll: {value}')
        except ValueError:
            await message.channel.send('Syntax is invalid, try again\n'
                                       'Valid syntax would look like: "dice <dice number> <number of rolls>"')

    if "character choice" in content:
        items = content.split("-")
        statindex = items.index("character choice")
        try:
            members[message.author.name] = player(items[statindex + 1], int(items[statindex + 2]), items[statindex + 3], int(items[statindex + 4]), int(items[statindex + 5]), int(items[statindex + 6]), int(items[statindex + 7]), int(items[statindex + 8]), int(items[statindex + 9]))
            await message.channel.send(f"Character created for {message.author.name}")
        except:
            await message.channel.send("Syntax invalid, please try again.\nValid Syntax: Character Choice-<name>-<level>-<race>(or subrace if applicable)-<strength>-<dexterity>-<constitution>-<intellect>-<wisdom>-<charisma>")

@client.command()
async def MyCharacter(ctx):
    await ctx.send(f"{ctx.author.name}'s {members[ctx.author.name].showStat()}")
client.run(TOKEN)