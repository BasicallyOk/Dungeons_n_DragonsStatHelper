class player:
    def __init__(self, name, level: int, race, strength: int, dexterity: int, constitution: int, intellect: int, wisdom: int, charisma: int):
        self.speed = 0
        self.leveling = [0, 2, 4, 6, 8, 11, 14, 17, 20, 24, 28, 32, 36, 41, 46, 51, 56, 62, 68, 74, 80]
        self.size = 0
        #self.role = role
        self.money = 0
        self.carryweight
        self.name = name
        self.level = level
        self.proficiency = self.leveling[self.level - 1]
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intellect = intellect
        self.wisdom = wisdom
        self.charisma = charisma
        self.ability = ""
        self.kin = race
        raceList = race.lower().split(' ')
        try:
            self.race = raceList[1]
            self.subrace = raceList[0]
        except IndexError:
            self.race = race.lower()
            self.subrace = None

        if self.race == 'elf':
            self.elves()
        if self.race == 'human':
            self.human()
        if self.race == 'dragonborn':
            self.dragonborn()
        if self.race == 'dwarf':
            self.dwarves()
        if self.race == 'gnome':
            self.gnome()

    def elves(self):
        self.dexterity += 2
        self.size = 'Medium'
        self.speed = 30
        self.ability = "\n-Darkvision (60 ft, can't discern colors)\n-Keen Senses: Proficiency in Perception\n-Fey Ancestry: You have advantage on saving throws against being charmed, and magic can’t put you to sleep.\n-Trance: Elves don't sleep, they only meditate for 4 hours, gaining full benefit of an 8-hour sleep.\n-Elf Weapon Training: Proficiency with longsword, shortsword, shortbow and long bow."
        if self.subrace == "high":
            self.intellect += 1
            self.ability += "\n-Cantrip: You know one cantrip of your choice from the wizard spell list. Intelligence is your spellcasting ability for it.\n-Extra language: You can speak, read, and write one extra language of your choice."
        if self.subrace == "wood":
            self.wisdom += 1
            self.speed = 35
            self.ability += "\n-Mask of the Wild: You can attempt to hide even when you are only lightly obscured by foliage, heavy rain, falling snow, mist, and other natural phenomena."
        else:
            print('Try again')

    def human(self):
        self.strength += 1
        self.dexterity += 1
        self.constitution += 1
        self.intellect += 1
        self.wisdom += 1
        self.charisma += 1
        self.size = 'Medium'
        self.speed = 30
        self.ability = "\n-Languages: You can speak, read, and write Common and one extra language of your choice. \nHumans typically learn the languages of other peoples they deal with, including obscure dialects. \nThey are fond of sprinkling their speech with words borrowed from other tongues: Orc curses, Elvish musical expressions, Dwarvish military phrases, and so on."

    def dragonborn(self):
        self.strength += 2
        self.speed = 30
        self.size = 'Medium'
        self.ability = '\n-Language: You can speak, read, and write Common and Draconic. Draconic is thought to be one of the oldest languages and is often used in the study of magic. The language sounds harsh to most other creatures and includes numerous hard consonants and sibilants.\n-Breath Weapon: You can use your action to exhale destructive energy. Your draconic ancestry determines the size, shape, and damage type of the exhalation. When you use your breath weapon, each creature in the area of the exhalation must make a saving throw, the type of which is determined by your draconic ancestry. The DC for this saving throw equals 8 + your Constitution modifier + your proficiency bonus. A creature takes 2d6 damage on a failed save, and half as much damage on a successful one. The damage increases to 3d6 at 6th level, 4d6 at 11th level, and 5d6 at 16th level. After you use your breath weapon, you can’t use it again until you complete a short or long rest.'
        if self.subrace == "black" or self.subrace == "copper":
            self.ability += ("\n-Damage resistance to Acid")
        if self.subrace == 'blue' or self.subrace == 'bronze':
            self.ability += ("\n-Damage resistance to Lightning")
        if self.subrace == 'brass' or self.subrace == 'gold' or self.subrace == 'red':
            self.ability += ("\n-Damage resistance to Fire")
        if self.subrace == 'green':
            self.ability += ("\n-Damage resistance to Poison")
        if self.subrace == 'silver' or self.subrace == 'white':
            self.ability += ("\n-Damage resistance to Cold")

    def dwarves(self):
        self.constitution += 2
        self.speed = 25
        self.size = 'Medium'
        self.ability = "\n-Darkvision (60ft range, can't discern colors)" \
                       "\n-Dwarven Resilience: You have advantage on saving throws against poison, and you have resistance against poison damage" \
                       "\n-Dwarven Combat Training: You have proficiency with the battleaxe, handaxe, light hammer, and warhammer." \
                       "\n-Tool Proficiency: You gain proficiency with the artisan’s tools of your choice: smith’s tools, brewer’s supplies, or mason’s tools." \
                       "\n-Stonecunning: Whenever you make an Intelligence (**History**) check related to the origin of stonework, you are considered proficient in the History skill and add double your proficiency bonus to the check, instead of your normal proficiency bonus." \
                       "\n-Languages: You can speak, read, and write Common and Dwarvish. Dwarvish is full of hard consonants and guttural sounds, and those characteristics spill over into whatever other language a dwarf might speak."
        if self.subrace == "hill":
            self.wisdom += 1
            self.ability += "\n-Dwarven Toughness: Your hit point maximum increases by 1, and it increases by 1 every time you gain a level."
        if self.subrace == 'mountain':
            self.strength += 2
            self.ability += "\n-Dwarven Armor Training: You have proficiency with light and medium armor."

    def gnome(self):
        self.intellect += 2
        self.size = 'small'
        self.speed = 25
        self.ability = "\n-Gnome Cunning: You have advantage on all Intelligence, Wisdom, and Charisma saving throws against magic."
        if self.subrace == 'deep':
            self.dexterity += 1
            self.ability += "\n-Superior Darkvision (120ft, can't discern color)" \
                            "\n-Stone Camouflage: You have advantage on Dexterity (Stealth) checks to hide in rocky terrain." \
                            "\n-Languages: You can speak, read, and write Common, Gnomish, and Undercommon. The svirfneblin dialect is more guttural than surface Gnomish, and most svirfneblin know only a little bit of Common, but those who deal with outsiders (and that includes you as an adventurer) pick up enough Common to get by in other lands."
        if self.subrace == 'rock':
            self.constitution += 1
            self.ability += "\n-Artificer's Lore: Whenever you make an Intelligence (History) check related to magic items, alchemical objects, or technological devices, you can add twice your proficiency bonus, instead of any proficiency bonus you normally apply." \
                            "\n-Tinker: You have proficiency with artisan’s tools (tinker’s tools). Using those tools, you can spend 1 hour and 10 gp worth of materials to construct a Tiny clockwork device (AC 5, 1 hp). The device ceases to function after 24 hours (unless you spend 1 hour repairing it to keep the device functioning), or when you use your action to dismantle it; at that time, you can reclaim the materials used to create it. You can have up to three such devices active at a time." \
                            "\n When you create a device, choose one of the following options:" \
                            "\n *Clockwork Toy*. This toy is a clockwork animal, monster, or person, such as a frog, mouse, bird, dragon, or soldier. When placed on the ground, the toy moves 5 feet across the ground on each of your turns in a random direction. It makes noises as appropriate to the creature it represents." \
                            "\n *Fire Starter*. The device produces a miniature flame, which you can use to light a candle, torch, or campfire. Using the device requires your action." \
                            "\n *Music Box*. When opened, this music box plays a single song at a moderate volume. The box stops playing when it reaches the song’s end or when it is closed."

    def showStat(self):
        return (f'level {self.level} {self.name}, {self.kin}-kin\nMovement Speed: {self.speed} ft, Size: {self.size}\nAbilities Scores:\nStrength: {self.strength}\nDexterity: {self.dexterity}\nConstitution: {self.constitution}\nIntellect: {self.intellect}\nWisdom: {self.wisdom}\nCharisma: {self.charisma}\nAbilities: {self.ability}')

    def levelUp(self):
        self.level += 1

    def abilityLevel(self, ability, n):
        for x in range(n):
            if ability == 'strength':
                self.strength += 1
            if ability == 'dexterity':
                self.dexterity += 1
            if ability == 'constitution':
                self.constitution += 1
            if ability == 'intellect':
                self.intellect += 1
            if ability == 'wisdom':
                self.wisdom += 1
            if ability == 'charisma':
                self.charisma += 1
            else: print('Please Try Again')

