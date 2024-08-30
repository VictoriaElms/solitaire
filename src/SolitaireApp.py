import tkinter as tk
from tkinter import PhotoImage
from src.deck import Deck
import os
import time


def move_stack(card, from_pile, to_pile):
    index = from_pile.index(card)
    to_pile.extend(from_pile[index:])
    del from_pile[index:]


class SolitaireApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.initial_tableau_states = None
        self.initial_waste_pile = None
        self.initial_stock_pile = None
        self.initial_foundations = None
        self.initial_tableau = None
        self.initial_deck = None
        self.undo_all_button = None
        self.vegas_mode_button = None
        self.undo_last_button = None
        self.foundation_frames = []
        self.tableau_frames = []
        self.foundations = [[] for _ in range(4)]
        self.waste_pile = []
        self.stock_pile = []
        self.score_label = None
        self.moves_label = None
        self.timer_label = None
        self.tableau = None
        self.new_game_button = None
        self.foundations_frame = None
        self.waste_pile_frame = None
        self.stock_pile_frame = None
        self.card_frames = None
        self.canvas = None
        self.title('Solitaire')
        self.geometry('1100x900')  # Increased width to give more space
        self.deck = Deck()
        self.image_refs = []  # Initialize image_refs here
        self.score = 0  # Initialize the score here
        self.vegas_mode = False  # Initialize vegas_mode flag
        self.cumulative_vegas_score = 0  # Initialize cumulative Vegas score
        self.start_time = time.time()  # Track the start time of the game
        self.moves = 0  # Initialize move counter
        self.game_over = False  # Flag to track if the game is over
        self.deck_passes = 0  # Track the number of passes through the deck

        # Load empty slot image
        self.empty_slot_image = PhotoImage(
            file=os.path.join(os.path.dirname(__file__), '..', 'assets', 'cards', 'sempty_slot.png'))

        self.create_tableau()  # Ensure this is called before setup_ui
        self.setup_ui()
        self.update_timer()  # Start the timer
        self.moves_history = []  # Initialize move history for undo functionality

    def setup_ui(self):
        self.canvas = tk.Canvas(self, width=1100, height=900, bg='green')
        self.canvas.pack(fill='both', expand=True)

        # Create frames for tableau, stockpile, waste pile, and foundation piles
        self.tableau_frames = []
        for i in range(7):
            frame = tk.Frame(self, width=120, height=600, bg='green', bd=0, highlightthickness=0)
            self.canvas.create_window(120 * i + 60, 250, anchor='nw', window=frame)
            self.tableau_frames.append(frame)

            # Adjust positions of the stockpile and waste pile to allow for 3-card draw spacing
            self.stock_pile_frame = tk.Frame(self, width=100, height=150, bg='green', bd=0, highlightthickness=0)
            self.canvas.create_window(50, 50, anchor='nw', window=self.stock_pile_frame)

            # Update the width of waste_pile_frame to give more space for displaying 3 cards
            self.waste_pile_frame = tk.Frame(self, width=100 + 2 * 20, height=150, bg='green', bd=0,
                                             highlightthickness=0)
            self.canvas.create_window(170, 50, anchor='nw', window=self.waste_pile_frame)

        # Adjust the x position to move foundation frames further to the right
        self.foundation_frames = []
        foundation_start_x = 370  # Moved further to the right to create more space for the 3-card draw
        for i in range(4):
            frame = tk.Frame(self, width=100, height=150, bg='green', bd=0, highlightthickness=0)
            self.canvas.create_window(foundation_start_x + 110 * i, 50, anchor='nw', window=frame)
            self.foundation_frames.append(frame)

        # Create New Game Button above the foundation boxes
        self.new_game_button = tk.Button(self, text="New Game", command=self.new_game)
        self.canvas.create_window(700, 10, anchor='nw', window=self.new_game_button)

        # Create Score Label
        self.score_label = tk.Label(self, text=f"Score: {self.score}", bg='green', fg='white', font=('Helvetica', 14))
        self.canvas.create_window(810, 10, anchor='nw', window=self.score_label)

        # Create Moves Label
        self.moves_label = tk.Label(self, text=f"Moves: {self.moves}", bg='green', fg='white', font=('Helvetica', 14))
        self.canvas.create_window(920, 10, anchor='nw', window=self.moves_label)

        # Create Timer Label
        self.timer_label = tk.Label(self, text="Time: 0:00", bg='green', fg='white', font=('Helvetica', 14))
        self.canvas.create_window(1030, 10, anchor='nw', window=self.timer_label)

        # Display cards in tableau
        self.display_tableau()
        self.display_stock_pile()
        self.display_waste_pile()
        self.display_foundations()

        # Create Undo Buttons at the bottom
        self.undo_all_button = tk.Button(self, text="Undo All Moves", command=self.undo_all_moves)
        self.canvas.create_window(300, 850, anchor='nw', window=self.undo_all_button)

        self.undo_last_button = tk.Button(self, text="Undo Last Move", command=self.undo_last_move)
        self.canvas.create_window(500, 850, anchor='nw', window=self.undo_last_button)

        # Toggle Vegas/Standard Mode Button
        self.vegas_mode_button = tk.Button(self, text="Switch to Vegas Mode", command=self.switch_to_vegas_mode)
        self.canvas.create_window(700, 850, anchor='nw', window=self.vegas_mode_button)

    def display_empty_slot(self, frame):
        empty_label = tk.Label(frame, image=self.empty_slot_image, bg='green', bd=0, highlightthickness=0)
        empty_label.pack()
        empty_label.bind('<Button-1>', lambda e: self.restock_from_waste())

    def update_timer(self):
        if not self.game_over:
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            self.timer_label.config(text=f"Time: {minutes}:{seconds:02d}")
            self.after(1000, self.update_timer)  # Update timer every second

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
                num_cards = len(self.tableau[i])
                # Calculate dynamic height needed for the frame
                frame_height = min(600, 30 * num_cards + 120)  # Minimum frame height adjusted
                frame.config(height=frame_height)  # Dynamically adjust frame height
                y_offset = min(30, frame_height // max(num_cards, 1))  # Dynamic offset to fit within the frame

                for j, card in enumerate(self.tableau[i]):
                    card_label = tk.Label(frame, image=card.display(), bd=0, highlightthickness=0)
                    card_label.place(x=0, y=y_offset * j)  # Adjust y to create cascading effect
                    card_label.bind('<Button-1>', lambda e, c=card, p=i: self.on_card_click(c, p))
                    self.image_refs.append(card.photo_image)
            else:
                self.display_empty_slot(frame)  # Display empty slot if tableau is empty

    def display_stock_pile(self):
        for widget in self.stock_pile_frame.winfo_children():
            widget.destroy()
        if self.stock_pile:
            # Show the back of the top card in the stock pile
            card = self.stock_pile[-1]
            card_label = tk.Label(self.stock_pile_frame, image=card.display(), bd=0, highlightthickness=0)
            card_label.pack()
            card_label.bind('<Button-1>', lambda e: self.flip_card())
            self.image_refs.append(card.photo_image)
        else:
            # Show the empty slot image if stockpile is empty
            self.display_empty_slot(self.stock_pile_frame)

    def display_waste_pile(self):
        for widget in self.waste_pile_frame.winfo_children():
            widget.destroy()
        if self.waste_pile:
            # Display the last 3 cards from the waste pile with overlapping
            if self.vegas_mode:
                # Ensure there's enough space for three cards to overlap
                for i, card in enumerate(self.waste_pile[-3:]):
                    card_label = tk.Label(self.waste_pile_frame, image=card.display(), bd=0, highlightthickness=0)
                    card_label.place(x=i * 30, y=0)  # Adjust x offset to create more visible overlap
                    self.image_refs.append(card.photo_image)
                    card_label.bind('<Button-1>',
                                    lambda e, c=card: self.on_card_click(c, -1))  # Use -1 to identify waste pile
            else:
                # In standard mode, only show the top card of the waste pile
                card = self.waste_pile[-1]
                card_label = tk.Label(self.waste_pile_frame, image=card.display(), bd=0, highlightthickness=0)
                card_label.pack()
                card_label.bind('<Button-1>',
                                lambda e, c=card: self.on_card_click(c, -1))  # Use -1 to identify waste pile
                self.image_refs.append(card.photo_image)

    def display_foundations(self):
        for i, frame in enumerate(self.foundation_frames):
            for widget in frame.winfo_children():
                widget.destroy()
            if self.foundations[i]:
                card = self.foundations[i][-1]
                card_label = tk.Label(frame, image=card.display(), bd=0, highlightthickness=0)
                card_label.pack()
                self.image_refs.append(card.photo_image)
            else:
                self.display_empty_slot(frame)

    def flip_card(self):
        if self.stock_pile:
            if self.vegas_mode:
                # Draw up to 3 cards and flip them in Vegas mode
                for _ in range(3):
                    if self.stock_pile:
                        card = self.stock_pile.pop()
                        card.flip()
                        self.waste_pile.append(card)
                        self.moves_history.append(('flip', card))
                        self.image_refs.append(card.photo_image)  # Keep a reference to the new image
            else:
                # Standard mode: draw one card
                card = self.stock_pile.pop()
                card.flip()
                self.waste_pile.append(card)
                self.moves_history.append(('flip', card))
                self.image_refs.append(card.photo_image)  # Keep a reference to the new image

            self.display_stock_pile()
            self.display_waste_pile()
        else:
            self.restock_from_waste()

    def restock_from_waste(self):
        if not self.stock_pile and self.waste_pile:
            self.deck_passes += 1
            self.stock_pile = self.waste_pile[::-1]
            self.waste_pile = []
            for card in self.stock_pile:
                card.flip()  # Flip all cards back face down
            if self.vegas_mode:
                self.update_score(-52)  # Subtract 52 points for reshuffling in Vegas mode
            self.display_stock_pile()
            self.display_waste_pile()

    def on_card_click(self, card, pile_index):
        if not card.is_face_up:
            # Only allow flipping if this card is the last face-down card in its pile
            if self.is_top_card(card, pile_index):
                card.flip()
                self.moves_history.append(('flip', card))
                self.display_tableau()
                self.update_moves(1)  # Increment move counter
            return

        if pile_index == -1:  # Clicked from waste pile
            for i, foundation in enumerate(self.foundations):
                if card.can_move_to_foundation(foundation):
                    self.foundations[i].append(card)
                    self.waste_pile.remove(card)
                    self.update_score(5)  # Increment score for moving card to foundation
                    self.moves_history.append(('move', card, -1, i, 'foundation'))
                    self.display_waste_pile()
                    self.display_foundations()
                    self.update_moves(1)  # Increment move counter
                    self.check_game_over()  # Check if game is over
                    return

            for i in range(7):
                if not self.tableau[i] and card.rank == 13:  # Move king to empty tableau pile
                    move_stack(card, self.waste_pile, self.tableau[i])
                    self.moves_history.append(('move', card, -1, i, 'tableau'))
                    self.display_tableau()
                    self.display_waste_pile()
                    self.update_moves(1)  # Increment move counter
                    return

                elif self.tableau[i] and card.can_stack_on(self.tableau[i][-1]):
                    move_stack(card, self.waste_pile, self.tableau[i])
                    self.update_score(5)  # Increment score for moving card in tableau
                    self.moves_history.append(('move', card, -1, i, 'tableau'))
                    self.display_tableau()
                    self.display_waste_pile()
                    self.update_moves(1)  # Increment move counter
                    return
            # Allow movement only if this is the topmost card in the tableau pile
        if pile_index != -1 and self.is_top_card(card, pile_index):
            for i, foundation in enumerate(self.foundations):
                if card.can_move_to_foundation(foundation):
                    self.foundations[i].append(card)
                    self.tableau[pile_index].remove(card)
                    self.update_score(5)  # Increment score for moving card to foundation
                    self.moves_history.append(('move', card, pile_index, i, 'foundation'))
                    self.display_tableau()
                    self.display_foundations()
                    self.update_moves(1)  # Increment move counter
                    self.check_game_over()  # Check if game is over
                    return

        for i in range(7):
            if i != pile_index and self.tableau[i] and card.can_stack_on(self.tableau[i][-1]):
                build_index = self.tableau[pile_index].index(card)
                if build_index == len(self.tableau[pile_index]) - 1:  # Ensure it's the top card
                    move_stack(card, self.tableau[pile_index], self.tableau[i])
                    self.update_score(5)  # Increment score for moving card in tableau
                    self.moves_history.append(('move', card, pile_index, i, 'tableau'))
                    self.display_tableau()
                    self.update_moves(1)  # Increment move counter
                    return

            if i != pile_index and not self.tableau[i] and card.rank == 13:  # Move king to empty tableau spot
                build_index = self.tableau[pile_index].index(card)
                if build_index == len(self.tableau[pile_index]) - 1:  # Ensure it's the top card
                    move_stack(card, self.tableau[pile_index], self.tableau[i])
                    self.update_score(5)  # Increment score for moving card in tableau
                    self.moves_history.append(('move', card, pile_index, i, 'tableau'))
                    self.display_tableau()
                    self.update_moves(1)  # Increment move counter
                    return

        if not self.tableau[pile_index] and card.rank == 13:  # Move king to empty tableau spot
            move_stack(card, self.tableau[pile_index], self.tableau[pile_index])
            self.update_score(5)  # Increment score for moving card in tableau
            self.moves_history.append(('move', card, pile_index, pile_index, 'tableau'))
            self.display_tableau()
            self.update_moves(1)  # Increment move counter

    def is_top_card(self, card, pile_index):
        """
        Check if the card is the top card in the tableau pile.
        """
        if pile_index == -1:
            return False
        pile = self.tableau[pile_index]
        return pile and pile[-1] == card

    def check_game_over(self):
        # Check if all cards are in foundations
        if all(len(foundation) == 13 for foundation in self.foundations):
            self.game_over = True
            self.display_game_over_message()

    def display_game_over_message(self):
        self.canvas.create_text(550, 450, text="GAME OVER", font=('Helvetica', 36, 'bold'), fill='red',
                                tags="game_over_text")

    def update_moves(self, increment):
        self.moves += increment
        self.moves_label.config(text=f"Moves: {self.moves}")

    def new_game(self):
        self.deck = Deck()
        self.create_tableau()
        self.foundations = [[] for _ in range(4)]  # Reset foundations
        self.waste_pile = []  # Reset waste pile
        self.stock_pile = self.deck.cards.copy()  # Use a copy to avoid modifying the original deck
        self.stock_pile = self.deck.cards  # Reset stock pile
        self.image_refs.clear()  # Clear old image references
        self.display_tableau()
        self.display_stock_pile()
        self.display_waste_pile()
        self.display_foundations()
        self.game_over = False  # Reset game over flag
        self.deck_passes = 0  # Reset deck passes counter
        if self.vegas_mode:
            self.score = -52  # Start with -52 points in Vegas mode
        else:
            self.score = 0  # Reset score
        self.start_time = time.time()  # Reset start time
        self.moves = 0  # Reset move counter
        self.update_score(0)  # Update score display
        self.update_moves(0)  # Update move display
        self.moves_history.clear()  # Clear move history

        # Remove any existing "Game Over" message
        self.canvas.delete("game_over_text")

        # Disable undo buttons in Vegas mode
        if self.vegas_mode:
            self.undo_last_button.config(state=tk.DISABLED)
            self.undo_all_button.config(state=tk.DISABLED)
        else:
            self.undo_last_button.config(state=tk.NORMAL)
            self.undo_all_button.config(state=tk.NORMAL)

        # Save the initial state of the game
        self.save_initial_state()

    def update_score(self, points):
        self.score += points
        self.score_label.config(text=f"Score: {self.score}")

    def calculate_time_bonus(self):
        end_time = time.time()
        total_time_seconds = end_time - self.start_time
        time_bonus = 700000 / total_time_seconds
        return time_bonus

    def undo_last_move(self):
        if not self.vegas_mode and self.moves_history:
            last_move = self.moves_history.pop()
            if last_move[0] == 'flip':
                card = last_move[1]
                card.flip()
                self.display_tableau()
                self.display_stock_pile()
                self.display_waste_pile()
            elif last_move[0] == 'move':
                card = last_move[1]
                from_pile_index = last_move[2]
                to_pile_index = last_move[3]
                pile_type = last_move[4]
                if pile_type == 'foundation':
                    self.foundations[to_pile_index].remove(card)
                    if from_pile_index == -1:
                        self.waste_pile.append(card)
                    else:
                        self.tableau[from_pile_index].append(card)
                elif pile_type == 'tableau':
                    self.tableau[to_pile_index].remove(card)
                    if from_pile_index == -1:
                        self.waste_pile.append(card)
                    else:
                        self.tableau[from_pile_index].append(card)
                self.display_tableau()
                self.display_foundations()
                self.display_waste_pile()
            self.update_moves(-1)  # Decrement move counter

    def save_initial_state(self):
        if not hasattr(self, 'initial_deck'):
            self.initial_deck = []
        if not hasattr(self, 'initial_tableau'):
            self.initial_tableau = []
        if not hasattr(self, 'initial_tableau_states'):
            self.initial_tableau_states = []

        self.initial_deck = self.deck.cards.copy()
        self.initial_tableau = [[card for card in pile] for pile in self.tableau]
        self.initial_foundations = [[] for _ in range(4)]
        self.initial_waste_pile = []
        self.initial_stock_pile = self.initial_deck.copy()
        # Capture the flipped state of each card in tableau
        self.initial_tableau_states = [[card.is_face_up for card in pile] for pile in self.tableau]

    def undo_all_moves(self):
        if not self.vegas_mode and hasattr(self, 'initial_deck'):
            # Restore the game state to the initial configuration
            self.deck.cards = self.initial_deck.copy()
            self.tableau = [[card for card in pile] for pile in self.initial_tableau]
            self.foundations = [pile.copy() for pile in self.initial_foundations]
            self.waste_pile = self.initial_waste_pile.copy()
            self.stock_pile = self.initial_stock_pile.copy()
            self.image_refs.clear()  # Clear old image references

            # Restore the flipped/unflipped state of each card in tableau
            for pile_index, pile in enumerate(self.tableau):
                for card_index, card in enumerate(pile):
                    initial_state = self.initial_tableau_states[pile_index][card_index]
                    card.is_face_up = initial_state
                    card.photo_image = card.load_image(card.front_image if card.is_face_up else card.back_image)

                    # Reset the stockpile to show cards face-down
        for card in self.stock_pile:
            card.is_face_up = False
            card.photo_image = card.load_image(card.back_image)

            self.display_tableau()
            self.display_stock_pile()
            self.display_waste_pile()
            self.display_foundations()
            self.game_over = False  # Reset game over flag
            self.moves = 0  # Reset move counter
            self.update_score(0)  # Reset score display
            self.update_moves(0)  # Reset moves display

            # Remove any existing "Game Over" message
            self.canvas.delete("game_over_text")

    def switch_to_vegas_mode(self):
        self.vegas_mode = not self.vegas_mode
        self.new_game()  # Start a new game in Vegas mode
        if self.vegas_mode:
            self.vegas_mode_button.config(text="Switch to Standard Mode")
        else:
            self.vegas_mode_button.config(text="Switch to Vegas Mode")

        # Redraw the waste pile based on the current mode
        self.display_waste_pile()

    def move_stack(self, card, from_pile, to_pile):
        index = from_pile.index(card)
        to_pile.extend(from_pile[index:])
        del from_pile[index:]


if __name__ == '__main__':
    app = SolitaireApp()
    app.mainloop()
