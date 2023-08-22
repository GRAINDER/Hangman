import random
import logging
import sqlite3
from typing import List, Dict
from visualisation import hangman_stages
from words import words_list

MAX_ATTEMPTS = 20

logging.basicConfig(level=logging.DEBUG, filename='hangman_data.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)




class Hangman: 
    """Attributes of the Hangman class"""
    def __init__(self):
        self.word_to_guess = "" # when game starts and new random word is genereated that word is bind to this variable. In the beginning it's empty string
        self.guessed_letters: Dict[str, bool] = {} # dictionary for guessed letter. Key is a letter, value is True/False if letter is correct or incorrect
        self.attempts = MAX_ATTEMPTS # number of attempts. Defined as 20 in start of code
        self.incorrect_guesses: List[str] = [] # list of incorrect guessed letters using for final result printing

    def get_random_word(self, words: List[str]) -> str:
        """Return a random word from the word list"""
        return random.choice(words) # using random library function to generate random word from defined word list

    def start_game(self):
        """Generating random word for Hangman game and displaying word in terminal"""
        self.word_to_guess = self.get_random_word(words_list)
        print("Welcome to Hangman!")
        print(self.display_word())

    def display_word(self) -> str:
        """Display the word with underscores for unguessed letters"""
        """Dictionary comprehension checking does guessed letter which is a key is in dictionary 
        and check status as value True/False and display full word using string gunction join"""
        return " ".join(letter if self.guessed_letters.get(letter, False) else "_" for letter in self.word_to_guess) # 

    def visualize_hangman(self) -> None:
        """Visualize the Hangman game status based on the number of attempts left"""
        hangman_stage = hangman_stages # importing list with visualisation from visualisaton.py file
        print(hangman_stage[20 - self.attempts])

    def validate_guess(self, guess: str) -> bool:
        """Validate user input and return True if it's a single letter or the correct full word, otherwise False."""
        if not guess.isalpha(): #Checking does user's input is letter if not letter then False
            return False
        if len(guess) == 1: #Checking does user's input is 1 letter and if this letter is in already gueassed letters dictionary
            return guess not in self.guessed_letters
        return True # length of guess is >= 2 letters and it's all alpha letter, so it's a word guess, so it's valid word guess

    def update_guess(self, guess: str) -> None:
        """Update the guessed letters and incorrect guesses based on the user's input"""
        if len(guess) == 1:
            if guess in self.word_to_guess:
                print("Correct guess!")
                logger.info("Correct guess!")
                self.guessed_letters[guess] = True
            else:
                print("Incorrect guess.")
                logger.info("Incorrect guess.")
                # self.guessed_letters[guess] = True
                self.incorrect_guesses.append(guess)
                self.attempts -= 1
        else:
            if guess == self.word_to_guess:
                # self.guessed_letters[guess] = True
                print(f"Congratulations! You guessed the word correctly! The word was {guess}")
                logger.info(f"Congratulations! You guessed the word correctly! The word was {guess}")
                self.guessed_letters = {letter: True for letter in self.word_to_guess} # check does user guessed full word is correct and if all key letters in list values are True, it means word is guessed
            else:
                print("Incorrect guess.")
                logger.info("Incorrect guess.")
                self.attempts -= 1 # if guess is not correct minus one life from all attempts

    def print_status(self):
        """Information about player's Hangman game status printing to terminal"""
        print(f"Attempts left: {self.attempts}")
        logger.info(f"Attempts left: {self.attempts}")
        self.visualize_hangman()
        print(self.display_word())
        logger.info(self.display_word())

    def is_game_over(self) -> bool:
        """Hangman game is over when user use all attemps for guessing letters or full word was guessed correc"""
        return self.attempts == 0 or all(self.guessed_letters.get(letter, False) for letter in self.word_to_guess) # function all() checks all letters in dict does values are True

    def end_the_game(self) -> Dict:
        """Calculating correct/incorrect guesses of player's game session"""
        num_correct_guesses = sum(1 for letter in self.guessed_letters if letter in self.word_to_guess and self.guessed_letters[letter]) # if conditions are met comprehension returns sequence of correct guesses (1) and sum it
        guesses_left = MAX_ATTEMPTS - len(self.incorrect_guesses)
        print("Games results:")

        print(f"Number of correct guesses: {num_correct_guesses}")
        print(f"Number of incorrect guesses: {len(self.incorrect_guesses)}")
        print(f"Number of guesses left: {guesses_left}")
        print(f"Incorrect guessed letters: {', '.join(self.incorrect_guesses)}")

        logger.info(f"Number of correct guesses: {num_correct_guesses}")
        logger.info(f"Number of incorrect guesses: {len(self.incorrect_guesses)}")
        logger.info(f"Number of guesses left: {guesses_left}")
        logger.info(f"Incorrect guessed letters: {', '.join(self.incorrect_guesses)}")

        game_result = {
            "num_correct_guesses": num_correct_guesses,
            "num_incorrect_guesses": len(self.incorrect_guesses),
            "guesses_left": guesses_left,
            "incorrect_guesses": self.incorrect_guesses
        }

        return game_result


class Player:
    """Getting all information about player"""
    def __init__(self):
        self.name = ""
        self.surname = ""
        self.email = ""

    def get_player_name(self):
        self.name = input("Enter your name: ")
        self.surname = input("Enter your surname: ")
        self.email = input("Enter your email: ")


class HangmanGame(Hangman, Player):
    def __init__(self):
        super().__init__()
        self.get_player_name()
        self.player_id = None
        self.initialize_database()

    def initialize_database(self):
        conn = sqlite3.connect("hangman.db")
        c = conn.cursor()

        # Create players table for database
        c.execute('''create table if not exists players (
                    id integer PRIMARY KEY,
                    name text,
                    surname text,
                    email text
                )''')

        # Create game_results table for database
        c.execute('''create table if not exists game_results (
                    id INTEGER PRIMARY KEY,
                    player_id integer,
                    correct_guesses integer,
                    incorrect_guesses integer,
                    guesses_left integer
                )''')

        conn.commit()
        conn.close()

    def create_player_record(self):
        conn = sqlite3.connect("hangman.db")
        c = conn.cursor()

        c.execute("INSERT INTO players (name, surname, email) VALUES (?, ?, ?)",
                  (self.name, self.surname, self.email))
        self.player_id = c.lastrowid

        conn.commit()
        conn.close()


    def play(self):
        self.create_player_record()

        while True:  # Add a loop for playing multiple games
            self.attempts = MAX_ATTEMPTS
            self.word_to_guess = ""
            self.guessed_letters = {}
            self.incorrect_guesses = []

            self.start_game()

            while not self.is_game_over():
                guess = input("Guess a letter or the entire word: ").lower()

                if guess in self.guessed_letters:
                    print("You already guessed this letter. Please try again.")
                    logger.info("You already guessed this letter. Please try again.")
                    continue

                if not self.validate_guess(guess):
                    print("Invalid input. Please try again.")
                    logger.info("Invalid input. Please try again.")
                    continue

                self.update_guess(guess)
                self.print_status()

            game_result = self.end_the_game()

            if self.attempts == 0:
                print(f"Game Over! You have exhausted all guesses. The correct word was '{self.word_to_guess}'.")
                logger.info(f"Game Over! The word was '{self.word_to_guess}'.")
                
            self.save_game_result(game_result)
            
            play_again = input("Do you want to play again? (yes/no): ").lower()
            if play_again != "yes":
                break  # Exit the loop if the player doesn't want to play again

    def save_game_result(self, game_result):
        conn = sqlite3.connect("hangman.db")
        c = conn.cursor()

        c.execute("INSERT INTO game_results (player_id, correct_guesses, incorrect_guesses, guesses_left) VALUES (?, ?, ?, ?)",
                    (self.player_id, game_result['num_correct_guesses'], game_result['num_incorrect_guesses'], game_result['guesses_left']))

        conn.commit()
        conn.close()


if __name__ == "__main__":
    try:
        hangman_game = HangmanGame()
        hangman_game.play()

    except KeyboardInterrupt:
        logger
