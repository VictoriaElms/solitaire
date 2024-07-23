import random
from src.card import Card
import os


class Deck:
    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cards_path = os.path.join(base_path, 'assets', 'cards')
        self.cards = []
        for suit in self.suits:
            for value in self.card_values:
                key = f"{value}_{suit}"
                image_name = Card.file_names[key]
                front_image_path = os.path.join(cards_path, image_name)
                back_image_path = os.path.join(cards_path, 'back.png')
                self.cards.append(
                    Card(suit, value, front_image_path, back_image_path)
                )
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop() if self.cards else None
