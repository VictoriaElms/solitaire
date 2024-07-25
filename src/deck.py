import random
from src.card import Card
import os

class Deck:
    suits = ['clubs', 'diamonds', 'hearts', 'spades']
    card_values = range(1, 14)  # 1 to 13

    def __init__(self):
        # Construct the path to the assets/cards directory relative to this file
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cards_path = os.path.join(base_path, 'assets', 'cards')
        self.cards = []
        for suit in self.suits:
            for value in self.card_values:
                # Construct the image filename based on the suit and value
                image_name = f'{suit[0]}{str(value).zfill(2)}.png'
                # Create the full path to the image file
                front_image_path = os.path.join(cards_path, image_name)
                back_image_path = os.path.join(cards_path, 'Card-Back-01.png')
                # Create a Card object with the front and back image paths
                self.cards.append(
                    Card(suit, str(value), front_image_path, back_image_path)
                )
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop() if self.cards else None