from helpers import GameSession
from argparse import ArgumentParser


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--lives", default=7, type=int, required=False)
    arg_parser.add_argument("--language", default="CS", type=str, required=False)

    args = arg_parser.parse_args()
    lives = args.lives
    language = args.language
    language_folder = "languages"

    session = GameSession(language_folder, language, lives)
    session.game_loop()


if __name__ == "__main__":
    main()
