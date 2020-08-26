class player:
    def __init__(self, name, level: int, race, strength: int, dexterity: int, constitution: int, intellect: int, wisdom: int, charisma: int):
        try:
            self.name = name
            self.level = level
            self.strength = strength
            self.dexterity = dexterity
            self.constitution = constitution
            self.intellect = intellect
            self.wisdom = wisdom
            self.charisma = charisma
            raceList = race.lower().split(' ')
            try:
                self.race = raceList[1]
                self.subrace = raceList[0]
            except IndexError:
                self.race = race.lower()
            switcher = {
                'elf': self.elves(self.subrace),
                'human':self.human()
            }
            switcher.get(self.race)

        except TypeError:
            print("Wrong value type")

    def showStat(self):
        return (f'level {self.level} {self.name}, {self.race}-kin\nMovement Speed: {self.speed} ft\nAbilities Scores:\nStrength: {self.strength}\nDexterity: {self.dexterity}\nConstitution: {self.constitution}\nIntellect: {self.intellect}\nWisdom: {self.wisdom}\nCharisma: {self.charisma}\nAbilities:{self.ability}')

    def elves(self, subrace):
        self.dexterity += 2
        self.size = 'Medium'
        self.speed = 30
        self.ability = "\n-Darkvision (60 ft, can't discern colors)\n-Keen Senses: Proficiency in Perception\n-Fey Ancestry: You have advantage on saving throws against being charmed, and magic can’t put you to sleep.\n-Trance: Elves don't sleep, they only meditate for 4 hours, gaining full benefit of an 8-hour sleep.\n-Elf Weapon Training: Proficiency with longsword, shortsword, shortbow and long bow."
        if subrace == "high":
            self.intellect += 1
            self.ability += "\n-Cantrip: You know one cantrip of your choice from the wizard spell list. Intelligence is your spellcasting ability for it.\n-Extra language: You can speak, read, and write one extra language of your choice."
        if subrace == "wood":
            self.wisdom += 1
            self.speed = 35
            self.ability += "\n-Mask of the Wild: You can attempt to hide even when you are only lightly obscured by foliage, heavy rain, falling snow, mist, and other natural phenomena."

    def human(self):
        pass

