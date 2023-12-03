import re
import numpy as np
import copy

green = []
yellow = []

def load_wordlists():
    words = []
    extwords = [] 
    with open("words.txt", "r") as file:
        for line in file:
            words.append(line.strip())
    with open("extwords.txt", "r") as file:
        for line in file:
            extwords.append(line.strip())
    return words, extwords

def basis(word):
    tempyellow = []
    for i in range(5):
        if word[i] == "g":
            if green[i] != '' and word[i+5] != green[i]:
                print("Invalid Input : Green Overlap")
                exit(0)
            if word[i+5] in yellow:
                yellow.remove(word[i+5])
            green[i] = word[i+5]
        elif word[i] == "y":
            tempyellow.append(word[i+5])
        elif word[i] != "b":
            print("Invalid Input : Invalid Colour of Letter")
            exit(0)
    for letter in tempyellow:
        if tempyellow.count(letter) > yellow.count(letter):
            yellow.extend([letter]*(tempyellow.count(letter) - yellow.count(letter)))
        if len(yellow) > green.count(""):
            print("Invalid Input : Too many Yellow Characters")
            exit(0)
               
def regex_generator(word):
    regex = []
    defaultregex = ["[a-z]"]*5
    curregex = copy.deepcopy(defaultregex)
    for i in range(5):
        if green[i] != "":
            curregex[i] = green[i]
    regex.append("".join(curregex))
    for i in range(5):
        curregex = copy.deepcopy(defaultregex)
        if word[i] == "y":
            curregex[i] = "[^" + word[i+5] + "]"
            regex.append("".join(curregex))
            regex.append(("[^{0}]*[{0}]"*yellow.count(word[i+5]) + ".*").format(word[i+5]))
        elif word[i] == "b":
            if word[i+5] in yellow:
                curregex[i] = "[^" + word[i+5] + "]"
                regex.append("".join(curregex))
            else:
                for j in range(5):
                    if green[j] == "":
                        curregex[j] = "[^" + word[i+5] + "]"
                regex.append("".join(curregex))
    return regex
         

def valid(words, extwords):
    while True:
        word = input("Please enter the word you guessed : ")
        if word == "exit":
            exit(0)
        word = word.replace(" ","").lstrip()
        if not re.match('^[bgy]{5}[a-z]{5}$', word):
            print("Sorry that formated was incorrect")
            continue
        else:
            print("Letter colours inputed is " + word[:5])
            print("Word inputed is " + word[5:])
            
        basis(word)
        regex = []
        regex = regex_generator(word)
        return [w for w in words if all(re.match(pattern, w) for pattern in regex)]
            
def best(words, extwords):
    best_words = {}
    standard = [[]]*5
    for word in words:
        for i in range(len(word)):
            standard[i].append(word[i])
    unknown_spaces = [i for i, x in enumerate(green) if x == ""]
    for word in extwords:
        best_words[word] = 0
        for i in unknown_spaces:
            multiplier = 1 / (word[:i].count(word[i])+1)
            if word[i] in yellow:
                best_words[word] += 2 * multiplier * (standard[i].count(word[i]) + standard.count(word[i])/5)
            else:
                best_words[word] += multiplier * (standard[i].count(word[i]) + standard.count(word[i])/5)
        if word in words:
            best_words[word] *= 1.5
        if best_words[word] < 0.01:
            del best_words[word]
        else :
            best_words[word] = best_words[word]/10
    sorted_best_words = sorted(best_words.items(), key=lambda x:x[1])[::-1]
    return sorted_best_words

if __name__ == "__main__":
    words, extwords = load_wordlists()
    print("\n\n\n")
    print("Please write a sequence of 5 letters made of 'b','y' or 'g' prior to your guessed word e.g. bbgyy smack")
    print("Type exit at anytime to leave")
    while True:
        cont = input("\nWould you like to enter a new word? (Y?N) : ")
        if cont == "N" or cont == "exit":
            break
        green = [""]*5
        yellow = []
        valid_words = words
        count = 1    
        while len(valid_words) > 1 and count < 6:
            valid_words = valid(valid_words, extwords)
            with open("valid_words.txt", "w") as file:
                file.write("\n".join(valid_words))
            best_words = best(valid_words, extwords)
            with open("best_words.txt", "w") as file:
                file.write("\n".join([x + " : " +str(y) for x, y in best_words]))
            count += 1
            print("Check valid_words.txt and best_words.txt")