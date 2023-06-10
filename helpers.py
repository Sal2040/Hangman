import random
from jinja2 import Environment, FileSystemLoader
from enum import Enum


class WordList:
    def __init__(self, text_file):
        self.__word_list = self.__read_text_file(text_file)

    @staticmethod
    def __read_text_file(file):
        with open(file, 'r') as f:
            result = f.read().splitlines()
        return result

    def get_random_word(self):
        return random.choice(self.__word_list)


class Word:
    def __init__(self, word: str):
        self.__word = word
        self.__correctly_guessed_letters = set()

    def __str__(self):
        return self.__word

    def return_word_len(self):
        return len(self.__word)

    def return_correctly_guessed_part(self):
        result = ""
        for letter in self.__word:
            if letter in self.__correctly_guessed_letters:
                result += letter
            else:
                result += " _ "
        return result

    def guess_letter(self, player, input_letter):
        letter = input_letter.lower()
        if letter in self.__word:
            # correct guess
            if letter not in self.__correctly_guessed_letters:
                self.__correctly_guessed_letters.add(input_letter)
                return 0
            else:
                # correct but repeated guess
                return 1
        else:
            # wrong guess
            player.remove_life()
            return 2

    def is_completed(self):
        return len(set(self.__word)) == len(self.__correctly_guessed_letters)


class Player:
    def __init__(self, lives=10):
        self.__lives = lives

    def return_lives(self):
        return self.__lives

    def remove_life(self):
        self.__lives -= 1

    def is_alive(self):
        return self.__lives > 0


class Game:
    def __init__(self, word, player, template_folder):
        self.__word = word
        self.__player = player
        self.__env = Environment(loader=FileSystemLoader(template_folder))
        self.__introduction = self.__env.get_template('introduction.txt')
        self.__first_input = self.__env.get_template('first_input.txt')
        self.__guess_letter = self.__env.get_template('guess_letter.txt')
        self.__remaining_lives = self.__env.get_template('remaining_lives.txt')
        self.__outro = self.__env.get_template('outro.txt')
        self.__answer_eval = self.__env.get_template('answer_eval.txt')

    def play(self):
        print(self.__introduction.render())
        input()
        context = {
            "word_len": self.__word.return_word_len(),
            "lives": self.__player.return_lives()
        }
        print(self.__first_input.render(context))
        print(self.__word.return_correctly_guessed_part())

        while self.__player.is_alive() and not self.__word.is_completed():
            input_letter = input(self.__guess_letter.render())
            result = self.__word.guess_letter(player=self.__player, input_letter=input_letter)
            context = {
                "result": result
            }
            print(self.__answer_eval.render(context))
            print(self.__word.return_correctly_guessed_part())
            context = {
                "lives": self.__player.return_lives()
            }
            print(self.__remaining_lives.render(context))

        context = {
            "alive": self.__player.is_alive(),
            "word": self.__word
        }
        print(self.__outro.render(context))
