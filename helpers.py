import random
from collections import defaultdict


class WordList:
    def __init__(self, text_file):
        self.__word_list = self.__read_text_file(text_file)

    @staticmethod
    def __read_text_file(file):
        result = []
        with open(file) as f:
            for line in f:
                result.append(line[:-1].lower())
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
            if letter not in self.__correctly_guessed_letters:
                self.__correctly_guessed_letters.add(input_letter)
                print("Správně!")
            else:
                print("Tohle písmeno jsi již uhodl.")
        else:
            player.remove_life()
            print("Špatně :(")

    def is_completed(self):
        if len(set(self.__word)) == len(self.__correctly_guessed_letters):
            return True
        else:
            return False


class Player:
    def __init__(self, lives=10):
        self.__lives = lives

    def return_lives(self):
        return self.__lives

    def remove_life(self):
        self.__lives -= 1

    def is_alive(self):
        if self.__lives > 0:
            return True
        else:
            return False


class Decliner:
    def __init__(self):
        self.pismeno = defaultdict(lambda: "písmen")
        self.pismeno[1] = "písmeno"
        for i in range(2, 5):
            self.pismeno[i] = "písmena"

        self.zivot = defaultdict(lambda: "životů")
        self.zivot[1] = "život"
        for i in range(2, 5):
            self.zivot[i] = "životy"

        self.zbyvat = defaultdict(lambda: "Zbývá")
        for i in range(2, 5):
            self.zbyvat[i] = "Zbývají"


class Game:
    def __init__(self, word, player, decliner):
        self.__word = word
        self.__player = player
        self.__decliner = decliner

    def play(self):
        print("Vítej ve hře Šibenice. Pokud chceš pokračovat, stiskni ENTER...")
        input()
        print(
            f"Hledané slovo má {self.__word.return_word_len()} {self.__decliner.pismeno[self.__word.return_word_len()]}.",
            f"{self.__decliner.zbyvat[self.__player.return_lives()]} ti {self.__player.return_lives()}"
            f" {self.__decliner.zivot[self.__player.return_lives()]}.",  # jak to zalomit?
            "Začínáme!",
        )
        print(self.__word.return_correctly_guessed_part())

        while self.__player.is_alive() and not self.__word.is_completed():
            input_letter = input("Hádej písmeno:")
            self.__word.guess_letter(player=self.__player, input_letter=input_letter)
            print(
                self.__word.return_correctly_guessed_part(),
                "\n",
                f"{self.__decliner.zbyvat[self.__player.return_lives()]} ti {self.__player.return_lives()} {self.__decliner.zivot[self.__player.return_lives()]}.",  # jak to zalomit?
            )

        if self.__player.is_alive():
            print("Gratulace, vyhrál jsi! \n")
        else:
            print("Tentokrát ti no nevyšlo... \n", f'To slovo mělo být "{self.__word}"')
