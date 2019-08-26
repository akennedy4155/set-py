# Copyright (c) 2019, Alex Kennedy
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import config as cfg
import itertools as itul
import random
from textwrap import dedent
from tabulate import tabulate


class Card:
    """
    Class that represents a card in the game of Set.
    """
    def __init__(self, color, texture, shape, number):
        """
        Initialize the card. The values passed in are expected to come from the card config.

        :param color: color of shapes on the card
        :type color: str
        :param texture: texture of shapes on the card
        :type texture: str
        :param shape: shapes on card
        :type shape: str
        :param number: number of shapes on the card
        :type number: str
        """
        self.card_params = {
            "color": color,
            "texture": texture,
            "number": number,
            "shape": shape
        }

    def __repr__(self):
        """
        :return: Representation of a card.
        :rtype: str
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


class Deck:
    """
    Class that represents a deck of :class:`Card` in the game of Set.  Contains a list of :class:`Card`.
    """
    def __init__(self):
        """
        Create all combinations of card params and shuffle them into the deck.
        """
        card_combos = list(itul.product(*cfg.card_config.values()))  # generate all combinations of attributes
        self.cards = [Card(*card_params) for card_params in card_combos]  # create the cards and put them into the deck
        self.shuffle()

    def shuffle(self):
        """
        Shuffle the remaining cards in the deck in a random order.
        """
        random.shuffle(self.cards)

    def peek(self, num=1):
        """
        Peek cards off the top of the deck without removing from the deck.

        :param num: Number of cards to peek off the deck.
        :type num: int
        :return: List of peeked cards.
        """
        peeked = self.cards[:num]
        return peeked
    
    def draw(self, num=1):
        """
        Draw cards off the top of deck, number specified by param.

        :param num: Number of cards to draw.
        :type num: int
        :return: Cards drawn from the deck.
        """
        popped = self.cards[:num]
        del self.cards[:num]
        return popped

    def __repr__(self):
        """
        :return: Representation of a deck.
        """
        return f"Deck with {len(self.cards)} cards remaining"


class Board:
    """
    Class that represents a board in the game of Set.  Contains a :class:`Deck` and a play area.
    """
    def __init__(self):
        self.deck = Deck()
        self.play_area = []
        for row in range(3):
            card_row = []
            for col in range(4):
                card_row.append(self.deck.draw())
            self.play_area.append(card_row)

    def get_cards_at_coords(self, coords):
        """
        Return the cards from the play area at the coordinates given in the arguments.
        Expects a list of 3 coordinate tuples (row, col) that lie within the play area (row < 3, col < 4).

        :param coords: List of 3 coordinate tuples of wanted cards.
        :type coords: list[tuple[int, int]]
        :return: 3 cards from the play area at the given coords.
        :rtype: list[Card]
        """
        return [self.play_area[row][col] for row,col in coords]
    
    def remove_and_fill(self, coords):
        # TODO: pass in a player to give the cards to for points
        """
        Remove cards from the play area (should be a Set) and refill with new cards from the deck.
        :param coords: Coords of cards to remove and fill with fresh cards from the Deck.
        :type coords: list[tuple[int, int]]
        """
        pass
    
    def __repr__(self):
        """
        :return: Representation of a board.
        """
        return f"Board:\n\n*{self.deck}*\n\nPlay Area:\n{tabulate(self.play_area, tablefmt='grid')}"


class Game:
    """
    Class representation of a game in Set.  Contains a :class:`Board` and TODO: players
    """
    def __init__(self):
        """
        Create a :class:`Board`.
        """
        self.board = Board()
    
    def is_set(self, coords):
        """
        Returns true if the cards at the coords given in params make up a Set.
        :param coords: Coordinates of the cards to check for Set.
        :type coords: list[tuple[int, int]]
        :return: True if cards at coordinates are a Set.
        """
        potential_set = self.board.getCards(coords)
        for category in cfg.card_config.keys():
            if not (self.all_same(potential_set, category) or self.all_different(potential_set, category)):
                return False
        return True

    def all_same(self, card_list, cat):
        """
        Returns true if all of the values for param cat in the list of cares are the same type.

        Example:

        oval, oval, oval -> True

        purple, green, purple -> False

        :param card_list: List of cards to check
        :type card_list: list[Card]
        :param cat: Category from the config dict to check.
        :type cat: str
        :return: True if all values of cat for card in list are the same.
        """
        cat_vals = [card.card_params[cat] for card in card_list]
        return len(set(cat_vals)) == 1

    def all_different(self, card_list, cat):
        """
        Returns true if all of the values for param cat in the list of cares are different types.

        Example:

        oval, squiggle, diamond -> True

        purple, green, purple -> False

        :param card_list: List of cards to check
        :type card_list: list[Card]
        :param cat: Category from the config dict to check.
        :type cat: str
        :return: True if all values of cat for card in list are the same.
        """
        cat_vals = [card.card_params[cat] for card in card_list]
        return len(set(cat_vals)) == 3