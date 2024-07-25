import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk


class Card:
    ranks = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12,
             'K': 13}
    suits = ['clubs', 'diamonds', 'hearts', 'spades']

    file_names = {
        '2_clubs': '2clubs.png',
        '3_clubs': '3clubs.png',
        '4_clubs': '4clubs.png',
        '5_clubs': '5clubs.png',
        '6_clubs': '6clubs.png',
        '7_clubs': '7clubs.png',
        '8_clubs': '8clubs.png',
        '9_clubs': '9clubs.png',
        '10_clubs': '10clubs.png',
        'J_clubs': 'jackclubs.png',
        'Q_clubs': 'queenclubs.png',
        'K_clubs': 'kingclubs.png',
        'A_clubs': 'aceclubs.png',

        '2_diamonds': '2diamonds.png',
        '3_diamonds': '3diamonds.png',
        '4_diamonds': '4diamonds.png',
        '5_diamonds': '5diamonds.png',
        '6_diamonds': '6diamonds.png',
        '7_diamonds': '7diamonds.png',
        '8_diamonds': '8diamonds.png',
        '9_diamonds': '9diamonds.png',
        '10_diamonds': '10diamonds.png',
        'J_diamonds': 'jackdiamonds.png',
        'Q_diamonds': 'queendiamonds.png',
        'K_diamonds': 'kingdiamonds.png',
        'A_diamonds': 'acediamonds.png',

        '2_hearts': '2hearts.png',
        '3_hearts': '3hearts.png',
        '4_hearts': '4hearts.png',
        '5_hearts': '5hearts.png',
        '6_hearts': '6hearts.png',
        '7_hearts': '7hearts.png',
        '8_hearts': '8hearts.png',
        '9_hearts': '9hearts.png',
        '10_hearts': '10hearts.png',
        'J_hearts': 'jackhearts.png',
        'Q_hearts': 'queenhearts.png',
        'K_hearts': 'kinghearts.png',
        'A_hearts': 'acehearts.png',

        '2_spades': '2spades.png',
        '3_spades': '3spades.png',
        '4_spades': '4spades.png',
        '5_spades': '5spades.png',
        '6_spades': '6spades.png',
        '7_spades': '7spades.png',
        '8_spades': '8spades.png',
        '9_spades': '9spades.png',
        '10_spades': '10spades.png',
        'J_spades': 'jackspades.png',
        'Q_spades': 'queenspades.png',
        'K_spades': 'kingspades.png',
        'A_spades': 'acespades.png'
    }

    def __init__(self, suit, value, front_image_path, back_image_path):
        self.suit = suit
        self.value = value
        self.rank = Card.ranks[value]
        self.front_image = front_image_path
        self.back_image = back_image_path
        self.is_face_up = False
        self.photo_image = self.load_image(self.back_image)  # Load back image initially

    def load_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((80, 120), Image.Resampling.LANCZOS)  # Resize image to fit the box
        return ImageTk.PhotoImage(image)

    def flip(self):
        self.is_face_up = not self.is_face_up
        self.photo_image = self.load_image(self.front_image if self.is_face_up else self.back_image)

    def display(self):
        return self.photo_image

    def is_red(self):
        return self.suit in ['hearts', 'diamonds']

    def is_black(self):
        return self.suit in ['clubs', 'spades']

    def can_stack_on(self, other_card):
        if not other_card:
            return False
        # Alternating colors and descending rank
        is_alternating_color = (self.is_red() and other_card.is_black()) or (self.is_black() and other_card.is_red())
        return is_alternating_color and self.rank == other_card.rank - 1

    def can_move_to_foundation(self, foundation):
        if not foundation:
            return self.rank == 1  # Ace
        return self.suit == foundation[-1].suit and self.rank == foundation[-1].rank + 1
