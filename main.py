import os
import discord
from discord.ext import commands
import random
from randomTowns import town
from player import Player
import races
import pickle

TOKEN =
client = commands.Bot(command_prefix = 'd.')
adventurers = {}
rolesDes = open("Roles", "r", encoding='utf8')
members = {}
final_role = {}  # Dict from UUIDs to Player objects


@client.event
async def on_ready():
    print("Campaign has started")


@client.command()
async def ping(ctx):
    await ctx.send('Whomst hast awakened the ancient one')


@client.command()
@commands.has_role("Dungeon Master")
async def roles(ctx):
    with open("Roles", "r", encoding='utf8') as role_descriptions:
        await ctx.send(role_descriptions.read())


@client.command()
async def memberslist(ctx):
    if len(final_role) == 0:
        await ctx.send("Wow, such an empty party. "
                       "Consider joining by sending .charCreate.")
        return
    await ctx.send("Party members list:")
    print(final_role)
    for user_id, player in final_role.items():
        await ctx.send(f"{client.get_user(user_id)} as {player}")


@client.event
async def on_message(message):
    global final_role
    if message.author == client.user:
        return

    if message.author.bot:
        return

    await client.process_commands(message)

    content = message.content.lower()


@client.command()
async def myCharacter(ctx):
    """Messages the user information about their character"""
    global final_role
    try:
        player = final_role[ctx.author.id]
        await client.get_user(ctx.author.id).send(player.showStat())
    except KeyError:
        await ctx.send('Your character might not have been created yet, use .newChar to create one')


@client.command()
async def dice(ctx, dice_str: str):
    """Takes an argument in traditional dice notation (2d6, 3d8, etc.) and returns the result of the rolls"""
    repeat = int(dice_str.split('d')[0])
    pips = int(dice_str.split('d')[1].split('+')[0])
    try:
        bonus = int(dice_str.split('d')[1].split('+')[1])
    except:
        bonus = 0
    if repeat > 20:
        raise ValueError('You may only roll up to 20 dice at once')
    response = '\n'.join(f'Dice Roll: {random.randint(1, pips)+bonus} (Added bonus of {bonus})\n' for _ in range(repeat))
    await ctx.send(response)


@dice.error
async def dice_error(ctx, error):
    await ctx.send(
        "Syntax is invalid, try again.\n"
        "You may roll up to 20 dice using the following syntax: `dice <number of rolls>d<dice number>+<bonus>`")


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
        await ctx.send(f"Congratulations! {ctx.author.name}'s {final_role[ctx.author.id].name} leveled up!\n"
                       f"Make sure you use stat_roll "
                       f"<strength> <dexterity> <constitution> <intellect> <wisdom> <charisma> "
                       f"to determine which abilities will be leveled up (the rest should be specified as 0) ")
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
@commands.has_role("Sutoriman-sensei")
async def loadGame(ctx):
    """Unpickles the saved final_role dict"""
    global final_role
    await ctx.send("Loading previous game file")
    try:
        with open('save_file', 'rb') as pickle_in:
            final_role = pickle.load(pickle_in)
        await ctx.send("Load complete. New adventurers can join in at any time using newChar command! Happy adventuring!")
    except FileNotFoundError:
        final_role = {}
        await ctx.send("Game file not found, creating an empty party")
    print(final_role)


@client.command()
@commands.has_role("Sutoriman-sensei")
async def saveGame(ctx):
    """Pickles final_role and saves it to a file"""
    await ctx.send("This action will overwrite your party's current save file, do you want to continue? "
                   "Respond with yes or no respond, action will be cancelled in 5 seconds (case sensitive)")

    def check(m: discord.Message):
        return m.author == ctx.message.author and m.channel == ctx.message.channel

    msg = await client.wait_for('message', check=check, timeout=5)
    if msg.content == 'yes':
        with open('save_file', 'wb') as pickle_out:
            pickle.dump(final_role, pickle_out)
        await ctx.send("Save complete")
    else:
        await ctx.send("Save cancelled")


@client.command()
async def newChar(ctx):
    user = ctx.author
    race = await get_race(user, user)
    role = await get_role(user, user)
    level = await get_level(user, user)
    name = await get_name(user, user)
    ability_scores = await get_ability_scores(user, user)

    player = Player(name, role, level, race, *ability_scores)
    final_role[user.id] = player
    print(player.showStat())
    await user.send(f'Character has been created for {user.name}, use myCharacter to view')

@client.command()
async def stat_roller(ctx):
    stats = [['💪', 'Strength'],
             ['🃏', 'Dexterity'],
             ['🏃', 'Constitution'],
             ['📖', 'Intelligence'],
             ['🧠', 'Wisdom'],
             ['💬', 'Charisma']]

    statName = [r[1] for r in stats]
    statEmoji = [r[0] for r in stats]
    message = '\n'.join(f'{statEmoji[i]}: {statName[i]}' for i in range(6))
    await ctx.send(f"React to the following 4d6 rolls (lowest will be omitted) with the corresponding emojis (This decision is final):"
                   f"{message}")
    results = []
    messageable = []
    choice = []
    for j in range(6):
        rolls = []
        for x in range(4):
            rolls.append(random.randint(1, 6))
        await sort(rolls)
        results.append(rolls[1] + rolls[2] + rolls[3])
        messageable.append(await ctx.send(f'Roll: {rolls[1]} + {rolls[2]} + {rolls[3]} = {rolls[1] + rolls[2] + rolls[3]} (omitted {rolls[0]} )'))

    for y in range(0, 6):
        print(messageable)
        choice.append(await(select_one_from_list(ctx, ctx.author, statName, statEmoji, messageable[y])))
        print(choice[y])

    try:
        final_role[ctx.author.id].strength += results[choice.index('Strength')]
        final_role[ctx.author.id].dexterity += results[choice.index('Dexterity')]
        final_role[ctx.author.id].constitution += results[choice.index('Constitution')]
        final_role[ctx.author.id].intelligence += results[choice.index('Intelligence')]
        final_role[ctx.author.id].wisdom += results[choice.index('Wisdom')]
        final_role[ctx.author.id].charisma += results[choice.index('Charisma')]

        await ctx.send (final_role[ctx.author.id].showStat())
    except KeyError:
        await ctx.send("Your character has not been created yet, please do so with newChar command")


async def sort(list):
    for iter_num in range(len(list) - 1, 0, -1):
        for idx in range(iter_num):
            if list[idx] > list[idx + 1]:
                temp = list[idx]
                list[idx] = list[idx + 1]
                list[idx + 1] = temp


async def get_race(messageable, author):
    """Prompts for character's race"""
    race_names = [cls.__name__ for cls in races.ALL_RACES]
    race_name_to_cls = {name: cls for name, cls in zip(race_names, races.ALL_RACES)}
    print(race_names)

    race_name = await select_one_from_list(messageable, author, race_names)
    race_cls = race_name_to_cls[race_name]
    # get subraces if possible
    try:
        subrace = await select_one_from_list(messageable, author, getattr(race_cls, 'subraces'))
    except AttributeError:
        subrace = ""

    race = await make_race(messageable, race_cls, subrace)
    return race


async def get_name(messageable, author):
    """Prompts for character's name"""
    await messageable.send("Enter your character's name:")

    def check(m: discord.Message):
        return m.author == author

    msg = await client.wait_for('message', check=check)
    return msg.content


async def get_role(messageable, author):
    """Prompts for character's class"""
    await messageable.send("Choose your character's class:")
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
    return await select_one_from_list(messageable, author, role_names, emojis=role_emojis)


async def get_level(messageable, author):
    await messageable.send("Enter the level of your class:")
    msg = await client.wait_for('message')
    level = int(msg.content)

    if level < 1:
        raise ValueError('level cannot be lower than 1.')

    return level


async def get_ability_scores(messageable, author):
    await messageable.send("Enter your ability scores separated by spaces:")

    def check(m: discord.Message):
        return m.author == author

    msg = await client.wait_for('message', check=check)
    ability_scores = [int(s) for s in msg.content.split(' ')]
    return ability_scores


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


async def select_one_from_list(messageable, author, lst, emojis=None, selection_message = None):
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

    if selection_message is None:
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
