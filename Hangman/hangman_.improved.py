import random
import logging
from typing import List, Dict
from visualisation import hangman_stages
from words import words_list

MAX_ATTEMPTS = 20

logging.basicConfig(level=logging.DEBUG,filename='hangman_data.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

# logging.basicConfig(level=logging.DEBUG)
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
    if not guess.isalpha():
        return False
    if len(guess) == 1:
        return guess not in guessed_letters
    # length of guess is >= 2 letters, so it's a word guess, so it's valid.
    return True


def hangman_game() -> None:
    # Pick a random word from the word list
    word_to_guess = get_random_word(words_list)
    guessed_letters: Dict[str, bool] = {}
    attempts = MAX_ATTEMPTS
    # max_attempts: int = 20
    # attempts: int = max_attempts
    incorrect_guesses: List[str] = []
    

    print("Welcome to Hangman!")
    print(display_word(word_to_guess, guessed_letters))

    hangman_game_main_loop(word_to_guess, guessed_letters, attempts, incorrect_guesses)
    if attempts == 0:
        print(f"Game Over! You have exhausted all guesses. The correct word was '{word_to_guess}'.")
        logger.info(f"Game Over! The word was '{word_to_guess}'.")
    
    end_the_game(word_to_guess, guessed_letters, incorrect_guesses)


def hangman_game_main_loop(word_to_guess, guessed_letters, attempts, incorrect_guesses):
    while attempts > 0:
        guess: str = input("Guess a letter or the entire word: ").lower()

        if guess in guessed_letters:
            print("You already guessed this letter. Please try again.")
            logger.info("You already guessed this letter. Please try again.")
            continue

        if not validate_guess(guess, word_to_guess, guessed_letters):
            print("Invalid input. Please try again.")
            logger.info("Invalid input. Please try again.")
            continue

        if len(guess) == 1:
            if guess in word_to_guess:
                print("Correct guess!")
                logger.info("Correct guess!")
                guessed_letters[guess] = True
            else:
                print("Incorrect guess.")
                logger.info("Incorrect guess.")
                guessed_letters[guess] = True  # Mark incorrect guesses as guessed to avoid repetition
                incorrect_guesses.append(guess)
                attempts -= 1  # Minus one attempt for incorrect letter guesses
        else:
            if guess == word_to_guess:
                print("Congratulations! You guessed the word correctly!")
                logger.info("Congratulations! You guessed the word correctly!")
                guessed_letters[guess] = True
                break
            else:
                print("Incorrect guess.")
                logger.info("Incorrect guess.")
                attempts -= 1
        print_status(word_to_guess, guessed_letters, attempts)

        # Check if all letters have been guessed
        if all(guessed_letters.get(letter, False) for letter in word_to_guess):
            print("Congratulations! You guessed all the letters correctly!")
            logger.info("Congratulations! You guessed all the letters correctly!")
            break


def print_status(word_to_guess, guessed_letters, attempts):
    print(f"Attempts left: {attempts}")
    logger.info(f"Attempts left: {attempts}")
    visualize_hangman(attempts)
    print(display_word(word_to_guess, guessed_letters))
    logger.info(display_word(word_to_guess, guessed_letters))

    
def end_the_game(word_to_guess, guessed_letters, incorrect_guesses):
    num_correct_guesses = sum(1 for letter in guessed_letters if letter in word_to_guess and guessed_letters[letter])
    # print(num_correct_guesses)
    # print(num_correct_guesses)
    # print(incorrect_guesses)
    guesses_left = MAX_ATTEMPTS - len(incorrect_guesses)
    print(f"Number of correct guesses: {num_correct_guesses}")
    print(f"Number of incorrect guesses: {len(incorrect_guesses)}")
    print(f"Number of guesses left: {guesses_left}")
    print(f"Incorrect guessed letters: {', '.join(incorrect_guesses)}")

    logger.info(f"Number of correct guesses: {num_correct_guesses}")
    logger.info(f"Number of incorrect guesses: {len(incorrect_guesses)}")
    logger.info(f"Number of guesses left: {guesses_left}")
    logger.info(f"Incorrect guessed letters: {', '.join(incorrect_guesses)}")



if __name__ == "__main__":
    try:
        hangman_game()
    except KeyboardInterrupt:
        logger.info("Game terminated by the user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
