import tkinter as tk
from src.deck import Deck
from tkinter import PhotoImage
import os
import time


def load_background_image():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    background_image_path = os.path.join(base_path, 'assets', 'cards', 'background.png')
    return PhotoImage(file=background_image_path)


class SolitaireApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.foundation_frames = []
        self.tableau_frames = []
        self.foundations = [[] for _ in range(4)]
        self.waste_pile = []
        self.stock_pile = []
        self.score_label = None
        self.tableau = None
        self.new_game_button = None
        self.foundations_frame = None
        self.waste_pile_frame = None
        self.stock_pile_frame = None
        self.card_frames = None
        self.canvas = None
        self.title('Solitaire')
        self.geometry('800x600')
        self.deck = Deck()
        self.image_refs = []  # Initialize image_refs here
        self.background_image = load_background_image()
        self.score = 0  # Initialize the score here
        self.start_time = time.time()  # Track the start time of the game
        self.create_tableau()  # Ensure this is called before setup_ui
        self.setup_ui()

    def setup_ui(self):
        self.canvas = tk.Canvas(self, width=900, height=800)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.background_image)

        # Create frames for tableau, stockpile, waste pile, and foundation piles
        self.tableau_frames = []
        for i in range(7):
            frame = tk.Frame(self, width=100, height=600, bg='green')
            self.canvas.create_window(110 * i + 50, 250, anchor='nw', window=frame)
            self.tableau_frames.append(frame)

        self.stock_pile_frame = tk.Frame(self, width=100, height=150, bg='green')
        self.canvas.create_window(50, 50, anchor='nw', window=self.stock_pile_frame)

        self.waste_pile_frame = tk.Frame(self, width=100, height=150, bg='green')
        self.canvas.create_window(170, 50, anchor='nw', window=self.waste_pile_frame)

        self.foundation_frames = []
        for i in range(4):
            frame = tk.Frame(self, width=100, height=150, bg='green')
            self.canvas.create_window(290 + 110 * i, 50, anchor='nw', window=frame)
            self.foundation_frames.append(frame)

        # Display cards in tableau
        self.display_tableau()

        # Create New Game Button
        self.new_game_button = tk.Button(self, text="New Game", command=self.new_game)
        self.canvas.create_window(700, 20, anchor='nw', window=self.new_game_button)

        # Create Score Label
        self.score_label = tk.Label(self, text=f"Score: {self.score}", bg='green', fg='white', font=('Helvetica', 14))
        self.canvas.create_window(600, 20, anchor='nw', window=self.score_label)

        self.display_stock_pile()
        self.display_waste_pile()
        self.display_foundations()

    def create_tableau(self):
        self.tableau = [[] for _ in range(7)]
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.deal()
                if card:
                    if j == i:
                        card.flip()
                    self.tableau[i].append(card)
        self.stock_pile = self.deck.cards

    def display_tableau(self):
        for i, frame in enumerate(self.tableau_frames):
            for widget in frame.winfo_children():
                widget.destroy()
            if self.tableau[i]:
                for j, card in enumerate(self.tableau[i]):
                    card_label = tk.Label(frame, image=card.display())
                    card_label.place(x=0, y=30 * j)  # Adjust y to create cascading effect
                    card_label.bind('<Button-1>', lambda e, c=card, p=i: self.on_card_click(c, p))
                    self.image_refs.append(card.photo_image)

    def display_stock_pile(self):
        for widget in self.stock_pile_frame.winfo_children():
            widget.destroy()
        if self.stock_pile:
            card = self.stock_pile[-1]
            card_label = tk.Label(self.stock_pile_frame, image=card.display())
            card_label.pack()
            card_label.bind('<Button-1>', lambda e, c=card: self.flip_card(c))
            self.image_refs.append(card.photo_image)

    def display_waste_pile(self):
        for widget in self.waste_pile_frame.winfo_children():
            widget.destroy()
        for i, card in enumerate(self.waste_pile):
            card_label = tk.Label(self.waste_pile_frame, image=card.display())
            card_label.pack()
            self.image_refs.append(card.photo_image)

    def display_foundations(self):
        for i, frame in enumerate(self.foundation_frames):
            for widget in frame.winfo_children():
                widget.destroy()
            if self.foundations[i]:
                for j, card in enumerate(self.foundations[i]):
                    card_label = tk.Label(frame, image=card.display())
                    card_label.grid(row=j, column=0)
                    self.image_refs.append(card.photo_image)

    def flip_card(self, card):
        if self.stock_pile:
            card = self.stock_pile.pop()
            card.flip()
            self.waste_pile.append(card)
            self.image_refs.append(card.photo_image)  # Keep a reference to the new image
            self.display_stock_pile()
            self.display_waste_pile()
            self.update_score(5)  # Increment score for flipping card from stockpile

    def on_card_click(self, card, pile_index):
        if not card.is_face_up:
            card.flip()
            self.update_score(5)  # Increment score for revealing a hidden card
            self.display_tableau()
            return

        for i, foundation in enumerate(self.foundations):
            if card.can_move_to_foundation(foundation):
                self.foundations[i].append(card)
                self.tableau[pile_index].remove(card)
                self.update_score(10)  # Increment score for moving card to foundation
                self.display_tableau()
                self.display_foundations()
                return

        for i in range(7):
            if i != pile_index and self.tableau[i] and card.can_stack_on(self.tableau[i][-1]):
                self.tableau[i].append(card)
                self.tableau[pile_index].remove(card)
                self.update_score(5)  # Increment score for moving card in tableau
                self.display_tableau()
                return

    def new_game(self):
        self.deck = Deck()
        self.create_tableau()
        self.foundations = [[] for _ in range(4)]  # Reset foundations
        self.waste_pile = []  # Reset waste pile
        self.stock_pile = self.deck.cards  # Reset stock pile
        self.image_refs.clear()  # Clear old image references
        self.display_tableau()
        self.display_stock_pile()
        self.display_waste_pile()
        self.display_foundations()
        self.score = 0  # Reset score
        self.start_time = time.time()  # Reset start time
        self.update_score(0)  # Update score display

    def update_score(self, points):
        self.score += points
        self.score_label.config(text=f"Score: {self.score}")

    def calculate_time_bonus(self):
        end_time = time.time()
        total_time_seconds = end_time - self.start_time
        time_bonus = 700000 / total_time_seconds
        return time_bonus


if __name__ == '__main__':
    app = SolitaireApp()
    app.mainloop()
