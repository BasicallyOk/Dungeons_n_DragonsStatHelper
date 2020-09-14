from weaponStats import gear


class Player:
    def __init__(self, name, role, level: int, race, strength: int, dexterity: int, constitution: int, intelligence: int, wisdom: int, charisma: int):
        self.speed = 0
        #self.leveling = [0, 2, 4, 6, 8, 11, 14, 17, 20, 24, 28, 32, 36, 41, 46, 51, 56, 62, 68, 74, 80]
        self.leveling = [2, 2, 2, 2, 3, 3, 3, 8, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6]
        self.size = 0
        self.role = role
        self.money = 0
        self.carryweight = 0
        self.name = name
        self.level = level
        self.proficiency = self.leveling[self.level - 1]
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.abilities = []
        self.inventory = {}

        self.race = race
        self.apply_race_attributes(race)

    def __str__(self):
        return f'{self.name} the {self.race} - level {self.level} {self.role}'

    def apply_race_attributes(self, race):
        self.size = race.size
        self.speed = race.speed
        self.abilities += race.abilities

        # apply ability score changes
        for name, change in race.ability_score_changes.items():
            setattr(self, name, getattr(self, name) + change)

    def showStat(self):
        return (f'{self.name} the {self.race}\n'
                f'Level {self.level} {self.role}\n'
                f'Proficiency Bonus: +{self.proficiency}\n'
                f'Movement Speed: {self.speed} ft, Size: {self.size}\n'
                f'Ability Scores:\n'
                f'Strength: {self.strength}\n'
                f'Dexterity: {self.dexterity}\n'
                f'Constitution: {self.constitution}\n'
                f'Intelligence: {self.intelligence}\n'
                f'Wisdom: {self.wisdom}\n'
                f'Charisma: {self.charisma}\n'
                f'Abilities:\n'
                f'{self.abilityString()}')

    def abilityString(self):
        return '\n'.join(f'-{ability}' for ability in self.abilities)

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

    def addMoney(self, amount):
        self.money += amount
        print(f"Player added {amount}")
        self.carryweight += float(self.money/50)
        print('Player exceeded amount, deducting')
        if self.carryweight > self.strength*15:
            self.money -= (self.carryweight - (self.strength*15))*50

    def addInventory(self, item: gear):
        if item.bought:
            if self.money < item.price or (self.carryweight + item.weight) > self.strength * 15 :
                return 'Player lacks money or carryweight'
            else:
                self.addMoney(-item.price)
        self.inventory[item.name] = item
        return f'Player has successfully added {item.name} to inventory'

    def addWeight(self, weight):
        self.carryweight += weight
        if self.carryweight > self.strength * 15:
            return 'Player lack strength and will be encumbered'



