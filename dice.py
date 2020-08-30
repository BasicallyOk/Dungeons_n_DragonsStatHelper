from random import randint


class Dice:
    def __init__(self, num_rolls=4, max_number=8):
        self.num_rolls = num_rolls
        self.max_number = max_number

    def roll(self):
        return [randint(1, self.max_number) for _ in range(self.num_rolls)]

    def __str__(self):
        return f'{self.num_rolls}d{self.max_number}'

