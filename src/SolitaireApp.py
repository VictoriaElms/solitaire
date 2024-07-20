import tkinter as tk
from tkinter import PhotoImage
from src.deck import Deck  # Correct import for Deck

class SolitaireApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Solitaire')
        self.geometry('800x600')
        self.deck = Deck()
        self.image_refs = []  # Initialize image_refs here
        self.create_tableau()
        self.setup_ui()

    def setup_ui(self):
        self.card_frames = []
        for i in range(7):  # 7 columns for the tableau
            frame = tk.Frame(self, width=100, height=200, bg='green')
            frame.grid(row=1, column=i, padx=5, pady=5)
            self.card_frames.append(frame)

        self.stock_pile_frame = tk.Frame(self, width=100, height=200, bg='green')
        self.stock_pile_frame.grid(row=0, column=0, padx=5, pady=5)

        # Create New Game Button
        self.new_game_button = tk.Button(self, text="New Game", command=self.new_game)
        self.new_game_button.grid(row=0, column=1, padx=5, pady=5)

        self.display_stock_pile()
        self.display_tableau()

    def create_tableau(self):
        self.tableau = [[] for _ in range(7)]
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.deal()
                if j == i:
                    card.flip()
                self.tableau[i].append(card)

    def display_tableau(self):
        for i, frame in enumerate(self.card_frames):
            for widget in frame.winfo_children():
                widget.destroy()
            for card in self.tableau[i]:
                card_label = tk.Label(frame, image=card.display())
                card_label.pack()
                self.image_refs.append(card.photo_image)  # Keep a reference

    def display_stock_pile(self):
        for widget in self.stock_pile_frame.winfo_children():
            widget.destroy()
        if self.deck.cards:
            card = self.deck.cards[-1]
            card_label = tk.Label(self.stock_pile_frame, image=card.display())
            card_label.pack()
            card_label.bind('<Button-1>', lambda e, card=card: self.flip_card(card))
            self.image_refs.append(card.photo_image)  # Keep a reference

    def flip_card(self, card):
        card.flip()
        self.image_refs.append(card.photo_image)  # Keep a reference to the new image
        self.display_stock_pile()

    def new_game(self):
        self.deck = Deck()
        self.create_tableau()
        self.image_refs.clear()  # Clear old image references
        self.display_tableau()
        self.display_stock_pile()

if __name__ == '__main__':
    app = SolitaireApp()
    app.mainloop()