import os
import discord
from discord.ext import commands
import random
from randomTowns import town
from player import Player
import races
import pickle

TOKEN =
client = commands.Bot(command_prefix = '.')
adventurers = {}
rolesDes = open("Roles", "r", encoding='utf8')
members = {}
final_role = {}  # Dict from UUIDs to Player objects

@client.event
async def on_ready():
    print("Campaign has started")

@client.command()
async def ping(ctx):
    await ctx.send('Whomst has awakened the ancient one')


@client.command()
@commands.has_role("Dungeon Master")
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
    global final_role
    if message.author == client.user:
        return

    if message.author.bot:
        return

    await client.process_commands(message)

    content = message.content.lower()

    if "stat_roll" in content:
        items = content.split(" ")
        statindex = items.index("stat_roll")
        try:
            final_role[message.author.id].strength += int(items[statindex + 1])
            final_role[message.author.id].dexterity += int(items[statindex + 2])
            final_role[message.author.id].constitution += int(items[statindex + 3])
            final_role[message.author.id].intelligence += int(items[statindex + 4])
            final_role[message.author.id].wisdom += int(items[statindex + 5])
            final_role[message.author.id].charisma += int(items[statindex + 6])
        except:
            await message.channel.send(
                "Syntax invalid, please try again.\n"
                "Valid Syntax: stat roll "
                "<strength> <dexterity> <constitution> <intellect> <wisdom> <charisma>")
        await message.channel.send("Abilitiy Scores updated")

@client.command()
async def myCharacter(ctx):
    global final_role
    try:
        player = final_role[ctx.author.id]
        await client.get_user(ctx.author.id).send(player.showStat())
    except KeyError:
        await ctx.send('Your character might not have been created yet, use .newChar to create one')


@client.command()
async def dice(ctx, dice_str: str):
    repeat = int(dice_str.split('d')[0])
    pips = int(dice_str.split('d')[1])

    if repeat > 20:
        raise ValueError('You may only roll up to 20 dice at once')
    response = '\n'.join(f'Dice Roll: {random.randint(1, pips)}' for _ in range(repeat))
    await ctx.send(response)


@dice.error
async def dice_error(ctx, error):
    await ctx.send(
        "Syntax is invalid, try again.\n"
        "You may roll up to 20 dice using the following syntax: `dice <number of rolls>d<dice number>`")


@client.command()
async def add_weight(ctx, weight: int):
    global final_role
    try:
        await ctx.send(final_role[ctx.author.id].carryweight(weight))
    except:
        await ctx.send("Something went horribly wrong, please try again")

@client.command()
async def level_up(ctx):
    global final_role
    try:
        final_role[ctx.author.id].level += 1
        await ctx.send(f"Congratulations! {ctx.author.name}'s {final_role[ctx.author.id].name} leveled up!\nMake sure you use stat_roll <strength> <dexterity> <constitution> <intellect> <wisdom> <charisma> to determine which abilities will be leveled up (the rest should be specified as 0) ")
    except:
        await ctx.send("Something went horribly wrong, please try again")

@client.command()
async def viewTownStock(ctx):
    shops = ['Blacksmith', 'Enchanter', 'Magic Weps', 'Jeweler', 'Alchemist']
    emojis = ['🔨', '🔮', '⚔', '💎', '👨‍🔬']
    await ctx.send(town.viewStocks(await select_one_from_list(ctx, ctx.message.author, shops, emojis)))


@client.command()
async def viewTownFolks(ctx):
    await ctx.send(town.viewAllShops())

@client.command()
@commands.has_role("Dungeon Master")
async def loadGame(ctx):
    global final_role
    await ctx.send("Loading previous game file")
    pickle_in = open("save_file", "rb")
    final_role = pickle.load(pickle_in)
    print(final_role)
    pickle_in.close()
    await ctx.send("Load complete. New adventurers can join in at any time using newChar command! Happy adventuring!")


@client.command()
@commands.has_role("Dungeon Master")
async def saveGame(ctx):
    await ctx.send("This action will overwrite your party's current save file, do you want to continue? Respond with yes or no respond, action will be cancelled in 5 seconds (case sensitive)")
    def check(m: discord.Message):
        return m.content == 'yes' and m.channel == ctx.message.channel

    msg = await client.wait_for('message', check = check, timeout = 5)
    if msg:
        pickle_out = open("save_file", "wb")
        pickle.dump(final_role, pickle_out)
        pickle_out.close()
        await ctx.send("Save complete")

@client.command()
async def newChar(ctx):
    race = await get_race(ctx)
    role = await get_role(ctx)
    name = await get_name(ctx)

    player = Player(name, role, 0, race, 0, 0, 0, 0, 0, 0)
    final_role[ctx.author.id] = player
    print(player.showStat())
    await ctx.send(f'Character has been created for {ctx.author.name}, use myCharacter to view')


async def get_race(ctx):
    race_names = [cls.__name__ for cls in races.ALL_RACES]
    race_name_to_cls = {name: cls for name, cls in zip(race_names, races.ALL_RACES)}
    print(race_names)

    race_name = await select_one_from_list(ctx, ctx.message.author, race_names)
    race_cls = race_name_to_cls[race_name]
    # get subraces if possible
    try:
        subrace = await select_one_from_list(ctx, ctx.message.author, getattr(race_cls, 'subraces'))
    except AttributeError:
        subrace = ""

    race = await make_race(ctx, race_cls, subrace)
    return race


async def get_name(ctx):
    """Prompts for user's name"""
    await ctx.send("Enter your character's name:")
    channel = ctx.message.channel

    def check(m: discord.Message):
        return m.author == ctx.message.author and m.channel == channel

    msg = await client.wait_for('message', check=check)
    return msg.content


async def get_role(ctx):
    """Prompts for character's class"""
    await ctx.send("Choose your character's class:")
    roles = [['barbarian', '🪓'],
             ['bard', '🎸'],
             ['cleric', '😇'],
             ['druid', '🌲'],
             ['fighter', '⚔'],
             ['monk', '☯'],
             ['paladin', '🛡'],
             ['ranger', '🏹'],
             ['rogue', '🃏'],
             ['sorcerer', '🔮'],
             ['warlock', '🧙'],
             ['wizard', '🧠']]
    role_names = [r[0].title() for r in roles]
    role_emojis = [r[1] for r in roles]
    return await select_one_from_list(ctx, ctx.message.author, role_names, emojis=role_emojis)


async def make_race(ctx, race_cls, subrace: str = ""):
    if race_cls == races.Elf:
        return races.Elf(subrace)
    if race_cls == races.Human:
        return races.Human()
    if race_cls == races.Dragonborn:
        return races.Dragonborn(subrace)
    if race_cls == races.Dwarf:
        return races.Dwarf(subrace)
    if race_cls == races.Gnome:
        # you've been gnomed
        return races.Gnome(subrace)
    if race_cls == races.Halfling:
        return races.Halfling(subrace)
    if race_cls == races.HalfOrc:
        return races.HalfOrc()
    if race_cls == races.Tiefling:
        return races.Tiefling()

    raise ValueError(f'race {race_cls} does not exist')


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
                selected.append(lst[emojis.index(str(react.emoji))])

    return selected


client.run(TOKEN)
