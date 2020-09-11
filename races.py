class Race:
    subrace = None

    def __str__(self):
        if self.subrace is None:
            return f'{type(self).__name__}'
        else:
            return f'{type(self).__name__} ({self.subrace})'

class Elf(Race):
    ability_score_changes = {
        'strength': 0,
        'dexterity': 2,
        'constitution': 0,
        'intelligence': 0,
        'wisdom': 0,
        'charisma': 0
    }
    size = 'medium'
    speed = 30
    subraces = ['high', 'wood', 'dark']

    abilities = ["Keen Senses: Proficiency in Perception", "Fey Ancestry: You have advantage on saving throws against being charmed, and magic can’t put you to sleep.", "Trance: Elves don't sleep, they only meditate for 4 hours, gaining full benefit of an 8-hour sleep."]

    def __init__(self, subrace):
        self.subrace = subrace

        if subrace == 'high':
            self.ability_score_changes['intelligence'] += 1
            self.abilities += ["Darkvision (60 ft, can't discern colors)", "Cantrip: You know one cantrip of your choice from the wizard spell list. Intelligence is your spellcasting ability for it.", "Extra language: You can speak, read, and write one extra language of your choice.", "Elf Weapon Training: Proficiency with longsword, shortsword, shortbow and long bow."]

        elif subrace == 'wood':
            self.ability_score_changes['wisdom'] += 1
            self.speed = 35
            self.abilities += ["Darkvision (60 ft, can't discern colors)", "Mask of the Wild: You can attempt to hide even when you are only lightly obscured by foliage, heavy rain, falling snow, mist, and other natural phenomena.", "Elf Weapon Training: Proficiency with longsword, shortsword, shortbow and long bow."]

        elif subrace == 'dark':
            self.ability_score_changes['charisma'] += 1
            self.abilities += ["Superior Darkvision (120ft, can't discern colors)", "Sunlight Sensitivity: You have disadvantage on attack rolls and on Wisdom(**Perception**) checks that rely on sight when you, the target of your attack, or whatever you are trying to perceive is in direct sunlight.", "Drow Magic: You know the *dancing lights* cantrip. When you reach 3rd level, you can cast the *faerie fire* spell once per day. When you reach 5th level, you can also cast the *darkness* spell once per day. Charisma is your spellcasting ability for these spells.", "Drow Weapon Training: You have proficiency with rapiers, shortswords, and hand crossbows."]

        else:
            raise ValueError(f'subrace {subrace} is not valid')


class Human(Race):
    ability_score_changes = {
        'strength': 1,
        'dexterity': 1,
        'constitution': 1,
        'intelligence': 1,
        'wisdom': 1,
        'charisma': 1
    }
    size = 'medium'
    speed = 30

    abilities = ["Languages: You can speak, read, and write Common and one extra language of your choice. \nHumans typically learn the languages of other peoples they deal with, including obscure dialects. \nThey are fond of sprinkling their speech with words borrowed from other tongues: Orc curses, Elvish musical expressions, Dwarvish military phrases, and so on."]


class Dragonborn(Race):
    ability_score_changes = {
        'strength': 2,
        'dexterity': 0,
        'constitution': 0,
        'intelligence': 0,
        'wisdom': 0,
        'charisma': 0
    }
    size = 'medium'
    speed = 30
    subraces = ['black', 'copper', 'blue', 'bronze', 'brass',
                'gold', 'red', 'green', 'silver', 'white']

    abilities = ["Language: You can speak, read, and write Common and Draconic. Draconic is thought to be one of the oldest languages and is often used in the study of magic. The language sounds harsh to most other creatures and includes numerous hard consonants and sibilants.", "Breath Weapon: You can use your action to exhale destructive energy. Your draconic ancestry determines the size, shape, and damage type of the exhalation. When you use your breath weapon, each creature in the area of the exhalation must make a saving throw, the type of which is determined by your draconic ancestry. The DC for this saving throw equals 8 + your Constitution modifier + your proficiency bonus. A creature takes 2d6 damage on a failed save, and half as much damage on a successful one. The damage increases to 3d6 at 6th level, 4d6 at 11th level, and 5d6 at 16th level. After you use your breath weapon, you can’t use it again until you complete a short or long rest."]

    def __init__(self, subrace):
        self.subrace = subrace

        if subrace not in self.subraces:
            raise ValueError(f'subrace {subrace} is not valid')

        if subrace in ('black', 'copper'):
            self.abilities += ["Damage resistance to Acid"]

        if subrace in ('blue', 'bronze'):
            self.abilities += ["Damage resistance to Lightning"]

        if subrace in ('brass', 'gold', 'red'):
            self.abilities += ["Damage resistance to Fire"]

        if subrace == 'green':
            self.abilities += ["Damage resistance to Poison"]

        if subrace in ('siver', 'white'):
            self.abilities += ["Damage resistance to Cold"]


class Dwarf(Race):
    ability_score_changes = {
        'strength': 0,
        'dexterity': 0,
        'constitution': 2,
        'intelligence': 0,
        'wisdom': 0,
        'charisma': 0
    }
    speed = 25
    size = 'medium'
    subraces = ['hill', 'mountain']

    abilities = ["Darkvision (60ft range, can't discern colors)",
                    "Dwarven Resilience: You have advantage on saving throws against poison, and you have resistance against poison damage",
                    "Dwarven Combat Training: You have proficiency with the battleaxe, handaxe, light hammer, and warhammer.",
                    "Tool Proficiency: You gain proficiency with the artisan’s tools of your choice: smith’s tools, brewer’s supplies, or mason’s tools.",
                    "Stonecunning: Whenever you make an Intelligence (**History**) check related to the origin of stonework, you are considered proficient in the History skill and add double your proficiency bonus to the check, instead of your normal proficiency bonus.",
                    "Languages: You can speak, read, and write Common and Dwarvish. Dwarvish is full of hard consonants and guttural sounds, and those characteristics spill over into whatever other language a dwarf might speak."]

    def __init__(self, subrace):
        self.subrace = subrace

        if subrace not in self.subraces:
            raise ValueError(f'subrace {subrace} is not valid')

        if subrace == 'hill':
            self.ability_score_change['wisdom'] += 1
            self.abilities += ["Dwarven Toughness: Your hit point maximum increases by 1, and it increases by 1 every time you gain a level."]

        if subrace == 'mountain':
            self.ability_score_changes['strength'] += 2
            self.abilities += ["Dwarven Armor Training: You have proficiency with light and medium armor."]


class Gnome(Race):
    ability_score_changes = {
        'strength': 0,
        'dexterity': 0,
        'constitution': 0,
        'intelligence': 2,
        'wisdom': 0,
        'charisma': 0
    }
    size = 'small'
    speed = 25
    subraces = ['deep', 'rock']

    abilities = ["Gnome Cunning: You have advantage on all Intelligence, Wisdom, and Charisma saving throws against magic."]

    def __init__(self, subrace):
        self.subrace = subrace

        if subrace not in self.subraces:
            raise ValueError(f'subrace {subrace} is not valid')

        if subrace == 'deep':
            self.ability_score_changes['dexterity'] += 1
            self.abilities += ["Superior Darkvision (120ft, can't discern color)",
                            "Stone Camouflage: You have advantage on Dexterity (Stealth) checks to hide in rocky terrain.",
                            "Languages: You can speak, read, and write Common, Gnomish, and Undercommon. The svirfneblin dialect is more guttural than surface Gnomish, and most svirfneblin know only a little bit of Common, but those who deal with outsiders (and that includes you as an adventurer) pick up enough Common to get by in other lands."]

        if subrace == 'rock':
            self.ability_score_changes['constitution'] += 1
            self.abilities += ["Artificer's Lore: Whenever you make an Intelligence (**History**) check related to magic items, alchemical objects, or technological devices, you can add twice your proficiency bonus, instead of any proficiency bonus you normally apply.",
                            "Tinker: You have proficiency with artisan’s tools (tinker’s tools). Using those tools, you can spend 1 hour and 10 gp worth of materials to construct a Tiny clockwork device (AC 5, 1 hp). The device ceases to function after 24 hours (unless you spend 1 hour repairing it to keep the device functioning), or when you use your action to dismantle it; at that time, you can reclaim the materials used to create it. You can have up to three such devices active at a time." \
                            "\n When you create a device, choose one of the following options:" \
                            "\n *Clockwork Toy*. This toy is a clockwork animal, monster, or person, such as a frog, mouse, bird, dragon, or soldier. When placed on the ground, the toy moves 5 feet across the ground on each of your turns in a random direction. It makes noises as appropriate to the creature it represents." \
                            "\n *Fire Starter*. The device produces a miniature flame, which you can use to light a candle, torch, or campfire. Using the device requires your action." \
                            "\n *Music Box*. When opened, this music box plays a single song at a moderate volume. The box stops playing when it reaches the song’s end or when it is closed."]


class Halfling(Race):
    ability_score_changes = {
        'strength': 0,
        'dexterity': 2,
        'constitution': 0,
        'intelligence': 0,
        'wisdom': 0,
        'charisma': 0
    }
    size = 'small'
    speed = 25
    subraces = ['lightfoot', 'stout']

    abilities = ["Lucky: When you roll a 1 on an attack roll, ability check, or saving throw, you can reroll the die and must use the new roll.",
                                        "Bravery: You have advantage on saving throws against being frightened.",
                                        "Halfling Nimbleness: You can move through the space of any creature that is of a size larger than yours.",
                                        "Languages: You can speak, read, and write Common and Halfling."]

    def __init__(self, subrace):
        self.subrace = subrace

        if subrace not in self.subraces:
            raise ValueError(f'subrace {subrace} is not valid')

        if subrace == 'lightfoot':
            self.ability_score_changes['charisma'] += 1
            self.abilities += ["Naturally Stealthy: You can attempt to hide even when you are obscured only by a creature that is at least one size larger than you."]

        if subrace == 'stout':
            self.ability_score_changes['constitution'] += 1
            self.abilities += ["Stout Resilience: You have advantage on saving throws against poison, and you have resistance against poison damage."]


class HalfOrc(Race):
    ability_score_changes = {
        'strength': 2,
        'dexterity': 0,
        'constitution': 1,
        'intelligence': 0,
        'wisdom': 0,
        'charisma': 0
    }
    size = 'medium'
    speed = 30

    abilities = ["Darkvision (60ft range, can't discern colors)",
                                        "Menacing: You gain proficiency in the Intimidation skill.",
                                        "Relentless Endurance: When you are reduced to 0 hit points but not killed outright, you can drop to 1 hit point instead. You can't use this feature again until you finish a long rest.",
                                        "Savage Attacks: When you score a critical hit with a melee weapon attack, you can roll one of the weapon's damage dice one additional time and add it to the extra damage of the critical hit.",
                                        "Languages: You can speak, read, and write Common and Orc."]


class Tiefling(Race):
    ability_score_changes = {
        'strength': 0,
        'dexterity': 0,
        'constitution': 0,
        'intelligence': 1,
        'wisdom': 0,
        'charisma': 2
    }
    size = 'medium'
    speed = 30

    abilities = ["Darkvision (60ft range, can't discern colors)",
                                        "Hellish Resistance: You have resistance to fire damage.",
                                        "Infernal Legacy: You know the *thaumaturgy* cantrip. Once you reach 3rd level, you can cast the *hellish rebuke* spell once per day as a 2nd-level spell. Once you reach 5th level, you can also cast the *darkness* spell once per day. Charisma is you spellcasting ability for these spells.",
                                        "Languages: You can speak, read, and write Common and Infernal."]


ALL_RACES = [Elf, Human, Dragonborn, Dwarf, Gnome,
                Halfling, HalfOrc, Tiefling]
