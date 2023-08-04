# hangman.py

import random
import logging
from typing import List, Dict
from visualisation import hangman_stages

from words import words_list

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_random_word(words: List[str]) -> str:
    """Return a random word from the word list."""
    return random.choice(words)

def display_word(word: str, guessed_letters: Dict[str, bool]) -> str:
    """Display the word with underscores for unguessed letters."""
    return " ".join(letter if guessed_letters.get(letter, False) else "_" for letter in word)

def visualize_hangman(attempts_left: int) -> None:
    """Visualize the hangman based on the number of attempts left."""
    hangman_stage = hangman_stages
    print(hangman_stage[20 - attempts_left])

def validate_guess(guess: str, word_to_guess: str, guessed_letters: Dict[str, bool]) -> bool:
    """Validate user input and return True if it's a single letter or the correct full word, otherwise False."""
    if len(guess) == 1 and guess.isalpha():
        return guess not in guessed_letters
    elif guess == word_to_guess and len(guess) > 1:
        return True
    return False

def hangman_game() -> None:
    # Pick a random word from the word list
    word_to_guess = get_random_word(words_list)
    guessed_letters: Dict[str, bool] = {}
    max_attempts: int = 20
    attempts: int = max_attempts
    incorrect_guesses: List[str] = []

    print("Welcome to Hangman!")
    print(display_word(word_to_guess, guessed_letters))

    while attempts > 0:
        guess: str = input("Guess a letter or the entire word: ").lower()

        if guess in guessed_letters:
            logger.info("You already guessed this letter. Please try again.")
            continue

        if not validate_guess(guess, word_to_guess, guessed_letters):
            logger.info("Invalid input. Please try again.")
            continue

        if len(guess) == 1:
            if guess in word_to_guess:
                logger.info("Correct guess!")
                guessed_letters[guess] = True
            else:
                logger.info("Incorrect guess.")
                guessed_letters[guess] = True  # Mark incorrect guesses as guessed to avoid repetition
                incorrect_guesses.append(guess)
                attempts -= 1  # Minus one attempt for incorrect letter guesses
        else:
            if guess == word_to_guess:
                logger.info("Congratulations! You guessed the word correctly!")
                guessed_letters[guess] = True
                break
            else:
                logger.info("Incorrect guess.")
                attempts -= 1

        logger.info(f"Attempts left: {attempts}")
        visualize_hangman(attempts)
        logger.info(display_word(word_to_guess, guessed_letters))

        # Check if all letters have been guessed
        if all(guessed_letters.get(letter, False) for letter in word_to_guess):
            logger.info("Congratulations! You guessed all the letters correctly!")
            break

    if attempts == 0:
        logger.info(f"Game Over! The word was '{word_to_guess}'.")
    
    num_correct_guesses = sum(guessed_letters.values())
    guesses_left = attempts - num_correct_guesses
    logger.info(f"Number of correct guesses: {num_correct_guesses}")
    logger.info(f"Number of guesses left: {guesses_left}")
    logger.info(f"Number of incorrect guesses: {len(incorrect_guesses)}")
    logger.info(f"Incorrect guessed letters: {', '.join(incorrect_guesses)}")

if __name__ == "__main__":
    try:
        hangman_game()
    except KeyboardInterrupt:
        logger.info("Game terminated by the user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
