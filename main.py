from helpers import WordList, Word, Player, Game
template_folder = "templates"

def main():
    wordlist = WordList(text_file="ceska_podstatna_jmena_test.txt")
    play_again = "A"
    while play_again == "A":
        word = Word(wordlist.get_random_word())
        player = Player(lives=10)
        game = Game(word=word, player=player, template_folder=template_folder)
        game.play()
        play_again = input("Hrát znovu?[A/N]")


if __name__=="__main__":
    main()
