# 6.00 Problem Set 2
# Name: Jorge Amaya
# Collaborators: None
# Time: 4:30

# Hangman
#


# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions

import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    #print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# load the list of words into the wordlist variable
# so that it can be accessed from anywhere in the program
wordlist = load_words()

#initial variables
secretWord = choose_word(wordlist)
guessesLeft = 8
availableLetters = 'abcdefghijklmnopqrstuvwxyz'
win = len(secretWord)

#variable to visualize correct guesses in the context of actual word
showWord = []
for i in range(len(secretWord)):
    showWord.append("_")

#introdution
print ""
print "Welcome to the game, Hangman!"
print "I am thinking of a word that is %d letters long" % len(secretWord)

#loop that terminates when you exhaust guesses or guess the word correctly
while guessesLeft > 0 or win == 0:
    print " " .join(showWord) #turns showWord from list to string to print nicely
    print ""
    print "You have %d guess(es) left" % guessesLeft
    print "Available letters: ", availableLetters
    
    guess = raw_input("Please guess a letter: ")
    guessLower = guess.lower()         

    #checks whether guess has been guessed or not        
    if guessLower in availableLetters:
        #incorrect answer
        if guessLower not in secretWord:
            print "Sorry, that letter is not in my word"
            guessesLeft -= 1
        #correct answer
        else:
            #see how many instances of the letter there are in the word
            howMany = secretWord.count(guessLower)
            win -= howMany
            #loop that replaces the '_' in the visualization of the word
            word = secretWord
            for i in range(howMany):
                find = word.index(guessLower)
                showWord[find] = guessLower
                word = word.replace(guessLower, "0", 1)   
            print "Good guess!"
            #couldn't figure out why the 'while' loop doesn't recognize when win == 0
            if win == 0:
                break
    else:
        print "Oops! you already guessed that letter"

    #removes guessed letter from availableLetters string
    availableLetters = availableLetters.replace(guessLower, '')
    
print ""
if win == 0: 
    print "Congratulations, you won!"
else:
    print "You did not win  the game"
print "The word is", secretWord
