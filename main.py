from helpers import WordList, Word, Player, Game
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
from argparse import ArgumentParser
import os
import sys


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--language", default="CS", required=False)

    args = arg_parser.parse_args()
    language = args.language
    language_u = language.upper()

    template_folder = os.path.join("templates", language_u)

    try:
        env = Environment(loader=FileSystemLoader(template_folder))
        yes = env.get_template("yes.txt")
        play_again = env.get_template("play_again.txt")
    except TemplateNotFound:
        try:
            language_l = language.lower()
            template_folder = os.path.join("templates", language_l)
            env = Environment(loader=FileSystemLoader(template_folder))
            yes = env.get_template("yes.txt")
            play_again = env.get_template("play_again.txt")
        except TemplateNotFound as e:
            sys.exit(f"Language '{language}' not supported.")

    wordlist = WordList(text_file="ceska_podstatna_jmena_test.txt")
    repeat_game = yes.render()
    while repeat_game == yes.render():
        word = Word(wordlist.get_random_word())
        player = Player(lives=10)
        game = Game(word=word, player=player, template_folder=template_folder)
        game.play()
        repeat_game = input(play_again.render())


if __name__=="__main__":
    main()
