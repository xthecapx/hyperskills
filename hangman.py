import random
from string import ascii_lowercase

class HangmanGame:
    def __init__(self, lives=8, languages=['python', 'java', 'kotlin', 'javascript']):
        self.languages = languages
        self.word = list(random.choice(self.languages))
        self.display = list('-' * len(self.word))
        self.lives = lives
        self.answers = set()

    def start_game(self):
        while self.lives > 0:
            display_word = ''.join(self.display)
            print('\n' + display_word)
            answer = input(f'Input a letter: ')
            prev_in_answer = answer in self.answers
            self.answers.add(answer)

            if 0 <= len(answer) > 1:
                print('You should input a single letter')
                continue

            if answer not in ascii_lowercase:
                print('It is not an ASCII lowercase letter')
                continue

            if len(self.answers) > 0 and prev_in_answer:
                print('You already typed this letter')
                continue

            if display_word.find('-') != -1:
                if answer in self.word:
                    for index, letter in enumerate(self.word):
                        if letter == answer:
                            self.display[index] = answer
                else:
                    print('No such letter in the word')
                    self.lives -= 1
            else:
                message = ''.join(self.word)
                print(f'You guessed the {message}!')
                print('You survived!')
                break
        else:
            print('You are hanged!')

    def turn_on(self):
        print('H A N G M A N\n')

        while True:
            menu = input('Type "play" to play the game, "exit" to quit:')

            if menu == 'play':
                self.start_game()
            elif menu == 'exit':
                break


game = HangmanGame()
game.turn_on()
