# PyWordleSolver

Command : python wordlesolver.py

When prompted for a word, put in colours (b,y,g) followed by the word you guessed. Example : "bbgby slope" if you guessed slope and had s, l and p as black, e as yellow and o as green.

Two documents are generated after you enter a word. valid_words.txt with all the valid words left from the information you gave. best_words.txt with what you should guess next along with a score using a heuristic.

Hope you find this useful!

Bug in Fix : When a letter is guessed as green but it reappers as yellow in a future guess, the valid word filter fails to capture it
