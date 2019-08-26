import config as cfg
import itertools as itul
import random
from textwrap import dedent
from tabulate import tabulate

class Card():
    """
    Class that represents a card in the game of set.

    Attributes:

        color (string): The color of the shapes on the card.
        texture (string): The texture of the shapes on the card.
        shape (string): The shapes on the card.
        number (string): The number of shapes on the card.
    """

    def __init__(self, color, texture, shape, number):
        """
        Card constructor.

        Parameters:
    
            color (string): The color of the shapes on the card.
            texture (string): The texture of the shapes on the card.
            number (string): The number of shapes on the card.
            shape (string): The shapes on the card.
        """
        self.card_params = {
            "color": color,
            "texture": texture,
            "number": number,
            "shape": shape
        }

    def __repr__(self):
        """
        Representation of a card.
        """
        return dedent(
            f"""\
            Card:

            Color: {self.card_params["color"]}
            Texture: {self.card_params["texture"]}
            Shape: {self.card_params["shape"]}
            Number: {self.card_params["number"]}
            """
        )

class Deck():
    def __init__(self):
        # generate all cards
        card_combos = list(itul.product(*cfg.card_config.values()))
        # put into the deck
        self.cards = [Card(*card_params) for card_params in card_combos]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def peek(self, num):
        return self.cards[:num]
    
    def draw(self, num = 1):
        popped = self.cards[:num]
        del self.cards[:num]
        return popped

    def __str__(self):
        return f"Deck with {len(self.cards)} cards remaining"

class Board():
    def __init__(self):
        self.deck = Deck()
        self.play_area = []
        for row in range(3):
            card_row = []
            for col in range(4):
                card_row.append(self.deck.draw())
            self.play_area.append(card_row)
    
    def __repr__(self):
        return f"Board:\n\n*{self.deck}*\n\nPlay Area:\n{tabulate(self.play_area, tablefmt='grid')}"

    def isSet(self, coords):
        potential_set = [self.play_area[row][col] for row,col in coords]
        for category in cfg.card_config.keys():
            if not (self.allSame(potential_set, category) or self.allDifferent(potential_set, category)):
                return False
        return True

    def allSame(self, card_list, cat):
        cat_vals = [card.card_params[cat] for card in card_list]
        return len(set(cat_vals)) == 1

    def allDifferent(self, card_list, cat):
        cat_vals = [card.card_params[cat] for card in card_list]
        return len(set(cat_vals)) == 3
    
    def takeSet(self):
        pass

    def fillBoard(self):
        pass


# b = Board()
# print(b)
# print([str(c) for c in d.peek(2)])

sample_list = [
    [0,1,2,3],
    [4,5,6,7],
    [8,9,10,11]
]

coords = [(0,1),(1,2),(2,3)]

print([sample_list[row][col] for row,col in coords])