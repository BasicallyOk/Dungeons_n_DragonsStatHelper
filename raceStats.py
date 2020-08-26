class player:
    def __init__(self, name, level: int, race, strength: int, dexterity: int, constitution: int, intellect: int, wisdom: int, charisma: int):
        self.speed = 0
        self.size = 0
        self.name = name
        self.level = level
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intellect = intellect
        self.wisdom = wisdom
        self.charisma = charisma
        self.ability = ""
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

    def elves(self):
        print("Elf is being used")
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

    def human(self):
        print('Human is being used')
        self.strength += 1
        self.dexterity += 1
        self.constitution += 1
        self.intellect += 1
        self.wisdom += 1
        self.charisma += 1
        self.size = 'Medium'
        self.speed = 30
        self.ability = "Languages: You can speak, read, and write Common and one extra language of your choice. \nHumans typically learn the languages of other peoples they deal with, including obscure dialects. \nThey are fond of sprinkling their speech with words borrowed from other tongues: Orc curses, Elvish musical expressions, Dwarvish military phrases, and so on."

    def showStat(self):
        return (f'level {self.level} {self.name}, {self.subrace} {self.race}-kin\nMovement Speed: {self.speed} ft, Size: {self.size}\nAbilities Scores:\nStrength: {self.strength}\nDexterity: {self.dexterity}\nConstitution: {self.constitution}\nIntellect: {self.intellect}\nWisdom: {self.wisdom}\nCharisma: {self.charisma}\nAbilities: {self.ability}')

