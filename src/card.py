import tkinter as tk
from tkinter import PhotoImage

class Card:
    def __init__(self, suit, value, front_image, back_image):
        self.suit = suit
        self.value = value
        self.front_image = front_image
        self.back_image = back_image
        self.is_face_up = False
        self.photo_image = PhotoImage(file=back_image)  # Load back image initially

    def flip(self):
        self.is_face_up = not self.is_face_up
        self.photo_image = PhotoImage(file=self.front_image if self.is_face_up else self.back_image)

    def display(self):
        return self.photo_image