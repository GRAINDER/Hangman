# Hangman
Fun Hangman game

Hangman is a classic word-guessing game where the player tries to guess a hidden word by suggesting letters one by one. The game has a limited number of attempts, and for each incorrect guess, a part of the hangman is drawn on the gallows. The objective is to guess the word before the hangman is fully drawn, or else the player loses the game.
How It Works
Game Rules

    1. The game randomly selects a word from a predefined list of words. The word to be guessed is represented by underscores, one for each letter in the word.

    2. The player has a maximum number of attempts to guess the word. By default, this number is set to 20, but it can be adjusted as desired.

    3. The player can make guesses in two ways: either by guessing a single letter or by attempting to guess the entire word.

    4. If the player guesses a letter that is part of the word, all occurrences of that letter in the word are revealed. If the guess is incorrect, the player loses one attempt.

    5. If the player chooses to guess the entire word, they must type the complete word. If the guess is correct, the player wins the game. If the guess is incorrect, the player loses one attempt.

    6. The player wins the game by correctly guessing all the letters of the word before running out of attempts.



Example Gameplay

Welcome to Hangman!

Word to guess: _ _ _ _ _ _

Guess a letter or the entire word: e
Incorrect guess. Attempts left: 19
Word to guess: _ _ _ _ _ _

Guess a letter or the entire word: a
Correct guess! Attempts left: 19
Word to guess: _ _ _ a _ _

Guess a letter or the entire word: i
Incorrect guess. Attempts left: 18
Word to guess: _ _ _ a _ _

Guess a letter or the entire word: programming
Congratulations! You guessed the word correctly!


Setup

To play the Hangman game:

    1. Clone this repository to your local machine.

    2. (Optional) Create a virtual environment and activate it.

    3. Run the hangman.py script in your terminal or command prompt using Python:
    
python hangman.py

1. The game will start, and you can begin guessing the letters or the entire word.. 


Requirements

The Hangman game is written in Python and uses built-in modules. No external packages are required.
Customization

You can customize the game by adding more words to the WORD_LIST in the hangman.py file or adjusting the maximum number of attempts by modifying the max_attempts variable.

Feel free to explore and modify the code to add new features or improve the user interface.

Have fun playing Hangman! Enjoy guessing the words and saving the hangman from being fully drawn! 🎉

Note: The above README provides a detailed overview of the Hangman game, including its rules, gameplay, setup instructions, requirements, and customization options. You can further enhance the README by adding images or GIFs to showcase the gameplay or any other relevant information to make it more appealing to potential users.
