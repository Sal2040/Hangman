from helpers import WordList, Word, Player, Game
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
from argparse import ArgumentParser
import os
import sys


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--lives", default=7, type=int, required=False)
    arg_parser.add_argument("--language", default="CS", type=str, required=False)

    args = arg_parser.parse_args()
    lives = args.lives
    language = args.language
    language_u = language.upper()

    template_folder = "templates"
    template_folder_path = os.path.join(template_folder, language_u)
    language_folder = "word_lists"
    language_file = language_u + ".txt"
    language_file_path = os.path.join(language_folder, language_file)

    try:
        env = Environment(loader=FileSystemLoader(template_folder_path))
        yes = env.get_template("yes.txt")
        no = env.get_template("no.txt")
        play_again = env.get_template("play_again.txt")
    except TemplateNotFound:
        try:
            language_l = language.lower()
            template_folder_path = os.path.join(template_folder, language_l)
            env = Environment(loader=FileSystemLoader(template_folder_path))
            yes = env.get_template("yes.txt")
            no = env.get_template("no.txt")
            play_again = env.get_template("play_again.txt")
        except TemplateNotFound:
            sys.exit(f"Language '{language}' not supported. Templates are missing")

    try:
        wordlist = WordList(text_file=language_file_path)
    except FileNotFoundError:
        try:
            language_l = language.lower()
            language_file = language_l + ".txt"
            language_file_path = os.path.join(language_folder, language_file)
            wordlist = WordList(text_file=language_file_path)
        except FileNotFoundError:
            sys.exit(f"Language '{language}' not supported. Corresponding list of words is missing.")

    repeat_game = yes.render()
    while repeat_game == yes.render():
        word = Word(wordlist.get_random_word())
        player = Player(lives=lives)
        game = Game(word=word, player=player, template_folder=template_folder_path)
        game.play()
        repeat_game = input(play_again.render())
        while repeat_game not in [yes.render(), no.render()]:
            repeat_game = input(play_again.render())


if __name__ == "__main__":
    main()
