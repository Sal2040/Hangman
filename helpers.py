import random
from jinja2 import Environment, FileSystemLoader
import os
import sys
from jinja2.exceptions import TemplateNotFound


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
        self.__word = word.lower()
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
    def __init__(self, word: Word, player: Player, templates: dict):
        self.__word = word
        self.__player = player
        self.__templates = templates

    def play(self):
        print(self.__templates["introduction"].render())
        input()
        context = {
            "word_len": self.__word.return_word_len(),
            "lives": self.__player.return_lives()
        }
        print(self.__templates["first_input"].render(context))
        print(self.__word.return_correctly_guessed_part())

        while self.__player.is_alive() and not self.__word.is_completed():
            input_letter = input(self.__templates["guess_letter"].render())
            result = self.__word.guess_letter(player=self.__player, input_letter=input_letter)
            context = {
                "result": result
            }
            print(self.__templates["answer_eval"].render(context))
            print(self.__word.return_correctly_guessed_part())
            context = {
                "lives": self.__player.return_lives()
            }
            print(self.__templates["remaining_lives"].render(context))

        context = {
            "alive": self.__player.is_alive(),
            "word": self.__word
        }
        print(self.__templates["outro"].render(context))


class GameSession:
    def __init__(self, language_folder, language):
        self.__wordlist, self.__templates = GameSession.fetch_language(language_folder, language)

    @staticmethod
    def fetch_templates(template_folder_path):
        env = Environment(loader=FileSystemLoader(template_folder_path))
        templates = {
            "introduction": env.get_template('introduction.txt'),
            "first_input": env.get_template('first_input.txt'),
            "guess_letter": env.get_template('guess_letter.txt'),
            "answer_eval": env.get_template('answer_eval.txt'),
            "remaining_lives": env.get_template('remaining_lives.txt'),
            "outro": env.get_template('outro.txt'),
            "yes": env.get_template("yes.txt"),
            "no": env.get_template("no.txt"),
            "play_again": env.get_template("play_again.txt")
                }
        return templates

    @staticmethod
    def fetch_language(language_folder, language):
        language_u = language.upper()
        language_l = language.lower()

        template_folder_path = os.path.join(language_folder, language_u, "templates")
        language_file = language_u + ".txt"
        language_file_path = os.path.join(language_folder, language_u, language_file)

        try:
            templates = GameSession.fetch_templates(template_folder_path)
        except TemplateNotFound:
            try:
                template_folder_path = os.path.join(language_folder, language_l, "templates")
                templates = GameSession.fetch_templates(template_folder_path)
            except TemplateNotFound:
                sys.exit(f"Language '{language}' not supported. Templates are missing")

        try:
            wordlist = WordList(text_file=language_file_path)
        except FileNotFoundError:
            try:
                language_file = language_l + ".txt"
                language_file_path = os.path.join(language_folder, language_l, language_file)
                wordlist = WordList(text_file=language_file_path)
            except FileNotFoundError:
                sys.exit(f"Language '{language}' not supported. Corresponding list of words is missing.")

        return wordlist, templates

    def game_loop(self, lives):
        yes = self.__templates["yes"].render()
        no = self.__templates["no"].render()
        play_again = self.__templates["play_again"].render()
        repeat_game = yes
        while repeat_game == yes:
            word = Word(self.__wordlist.get_random_word())
            player = Player(lives=lives)
            game = Game(word=word, player=player, templates=self.__templates)
            game.play()
            repeat_game = input(play_again)
            while repeat_game not in [yes, no]:
                repeat_game = input(play_again)
