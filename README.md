# Hangman

This is a simple implementation of the popular Hangman game in Python. It uses a CLI with text prompts and messages only. No actual drawing of the hangman figure is included.
The game supports multiple languages via `jinja2` templating.

## Project composition:
* **helpers.py** - module with functional classes
* **main.py** - main script to run the game
* **languages** - folder containing templates and wordlists


## Requirements
* Python 3.6+
* pip

## Usage:
1. Clone the repository
```bash
git clone https://github.com/Sal2040/Hangman
```

2. Install dependencies:
```bash
pip install -r <path_to_your_directory>/Hangman/requirements.txt
```

3. Run the game
```bash
python3 main.py [--language <language>] [--lives <number_of_lives>]
```
### Optional Arguments:  
```
--language    The language used in the script. Defaults to 'CS'.  
--lives       The number of lives. Defaults to 7.
```
## Language support:
* The game currently supports Czech ('CS') and English ('EN') language. There is a vocabulary of 50 most used nouns to guess from.  
* You can easily add other languages. Just create a new subdirectory in the `languages` directory and follow the same structure of templates and wordlist.