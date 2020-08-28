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
        await roll_dice(message)

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

async def roll_dice(message):
    content = message.content
    contentList = content.split(" ")
    try:
        num = int(contentList[contentList.index('dice') + 1])
        repeat = int(contentList[contentList.index('dice') + 2])

        if repeat > 25:
            raise ValueError
    except (IndexError, ValueError):
        await message.channel.send('Syntax is invalid, try again\n'
                                   'Valid syntax would look like: "dice <dice number> <number of rolls>"')
        return

    try:
        response = '\n'.join(f'Dice Roll: {random.randint(1, num)}' for _ in range(repeat))
        await message.channel.send(response)
    except ValueError:
        await message.channel.send('Syntax is invalid, try again\n'
                                   'Valid syntax would look like: "dice <dice number> <number of rolls>"')


async def select_one_from_list(messageable, author, lst, emojis=None):
    """
    Lets a discord user select an item from a list using reactions.
    Returns the selected item.
    Can raise ValueError and asyncio.TimeoutError.
    """
    if emojis is None:
        emojis = ['0️⃣',
            '1️⃣',
            '2️⃣',
            '3️⃣',
            '4️⃣',
            '5️⃣',
            '6️⃣',
            '7️⃣',
            '8️⃣',
            '9️⃣']
        emojis = emojis[:len(lst)]

    if len(lst) != len(emojis):
        raise ValueError(f'Lengths of lst and emojis are not equal ({len(lst)} != {len(emojis)})')

    # concatenate each line into a single message before sending
    messages = []
    for emoji, item in zip(emojis, lst):
        messages.append(f'{emoji} {item}')
    selection_message = await messageable.send('\n'.join(messages))

    # react with one emoji for each item
    for emoji in emojis:
        await selection_message.add_reaction(emoji)

    # wait for confirmation from author
    def check(reaction, user):
        return user == author and reaction.message.id == selection_message.id and str(reaction.emoji) in emojis

    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

    selected = lst[emojis.index(str(reaction.emoji))]
    return selected


async def select_multiple_from_list(messageable, author, lst, emojis=None):
    """
    Lets a discord user select multiple items from a list using reactions.
    Returns the selected items.
    Can raise ValueError and asyncio.TimeoutError.
    """
    if emojis is None:
        emojis = ['0️⃣',
            '1️⃣',
            '2️⃣',
            '3️⃣',
            '4️⃣',
            '5️⃣',
            '6️⃣',
            '7️⃣',
            '8️⃣',
            '9️⃣']
        emojis = emojis[:len(lst)]

    if len(lst) != len(emojis):
        raise ValueError(f'Lengths of lst and emojis are not equal ({len(lst)} != {len(emojis)})')

    # concatenate each line into a single message before sending
    messages = []
    for emoji, item in zip(emojis, lst):
        messages.append(f'{emoji} {item}')
    selection_message = await messageable.send('\n'.join(messages))

    # react with one emoji for each item
    for emoji in emojis:
        await selection_message.add_reaction(emoji)

    await selection_message.add_reaction('✅')

    # wait for confirmation from author
    def check(reaction, user):
        return user == author and reaction.message.id == selection_message.id and str(reaction.emoji) == '✅'

    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

    selected = []
    for react in reaction.message.reactions:
        if str(react.emoji) in emojis:
            if author in await react.users().flatten():
                selected.append( lst[emojis.index(str(react.emoji))] )

    return selected


client.run(TOKEN)
