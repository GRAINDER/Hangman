import random
import logging
from typing import List, Dict
from visualisation import hangman_stages
from words import words_list

MAX_ATTEMPTS = 20

logging.basicConfig(level=logging.DEBUG, filename='hangman_data.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)


class Hangman:
    def __init__(self):
        self.word_to_guess = ""
        self.guessed_letters: Dict[str, bool] = {}
        self.attempts = MAX_ATTEMPTS
        self.incorrect_guesses: List[str] = []

    def start_game(self):
        self.word_to_guess = self.get_random_word(words_list)
        print("Welcome to Hangman!")
        print(self.display_word())

    def get_random_word(self, words: List[str]) -> str:
        """Return a random word from the word list."""
        return random.choice(words)

    def display_word(self) -> str:
        """Display the word with underscores for unguessed letters."""
        return " ".join(letter if self.guessed_letters.get(letter, False) else "_" for letter in self.word_to_guess)

    def visualize_hangman(self) -> None:
        """Visualize the hangman based on the number of attempts left."""
        hangman_stage = hangman_stages
        print(hangman_stage[20 - self.attempts])

    def validate_guess(self, guess: str) -> bool:
        """Validate user input and return True if it's a single letter or the correct full word, otherwise False."""
        if not guess.isalpha():
            return False
        if len(guess) == 1:
            return guess not in self.guessed_letters
        # length of guess is >= 2 letters, so it's a word guess, so it's valid.
        return True

    def update_guess(self, guess: str) -> None:
        """Update the guessed letters and incorrect guesses based on the user's input."""
        if len(guess) == 1:
            if guess in self.word_to_guess:
                print("Correct guess!")
                logger.info("Correct guess!")
                self.guessed_letters[guess] = True
            else:
                print("Incorrect guess.")
                logger.info("Incorrect guess.")
                self.guessed_letters[guess] = True
                self.incorrect_guesses.append(guess)
                self.attempts -= 1
        else:
            if guess == self.word_to_guess:
                print("Congratulations! You guessed the word correctly!")
                logger.info("Congratulations! You guessed the word correctly!")
                self.guessed_letters[guess] = True
            else:
                print("Incorrect guess.")
                logger.info("Incorrect guess.")
                self.attempts -= 1

    def print_status(self):
        print(f"Attempts left: {self.attempts}")
        logger.info(f"Attempts left: {self.attempts}")
        self.visualize_hangman()
        print(self.display_word())
        logger.info(self.display_word())

    def is_game_over(self) -> bool:
        return self.attempts == 0 or all(self.guessed_letters.get(letter, False) for letter in self.word_to_guess)

    def end_the_game(self) -> Dict:
        num_correct_guesses = sum(1 for letter in self.guessed_letters if letter in self.word_to_guess and self.guessed_letters[letter])
        guesses_left = MAX_ATTEMPTS - len(self.incorrect_guesses)
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
    def __init__(self):
        self.name = ""

    def get_player_name(self):
        self.name = input("Enter your name: ")


class HangmanGame(Hangman, Player):
    def __init__(self):
        super().__init__()
        self.get_player_name()

    def play(self):
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

        return game_result


if __name__ == "__main__":
    try:
        hangman_game = HangmanGame()
        game_result = hangman_game.play()

        # Access the game result here and print or use it as needed
        print("Game Result:")
        print(game_result)

    except KeyboardInterrupt:
        logger.info("Game terminated by the user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
