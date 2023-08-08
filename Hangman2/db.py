import sqlite3
from hangman_v2 import Hangman, Player


class HangmanGame(Hangman, Player):
    def __init__(self):
        super().__init__()
        self.get_player_name()
        self.player_id = None
        self.initialize_database()

    def initialize_database(self):
        conn = sqlite3.connect("hangman.db")
        c = conn.cursor()

        # Create players table
        c.execute('''CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    surname TEXT,
                    email TEXT
                )''')

        # Create game_results table
        c.execute('''CREATE TABLE IF NOT EXISTS game_results (
                    id INTEGER PRIMARY KEY,
                    player_id INTEGER,
                    correct_guesses INTEGER,
                    incorrect_guesses INTEGER,
                    guesses_left INTEGER
                )''')

        conn.commit()
        conn.close()

    # ... rest of the methods remain the same
