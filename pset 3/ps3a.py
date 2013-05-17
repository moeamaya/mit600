# 6.00 Problem Set 3A Solutions
#
# The 6.00 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
#
# Name: Jorge Amaya
# Collaborators: None
# Time: 4:00


import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
handsize = 6

letterValue = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first go.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """

    total = 0

    #loops through each letter finding value and adding to total
    for letter in word:
        value = letterValue[letter]
        total += value

    #multiply total * word length
    total = total*len(word)

    #if word length is equal to hand size
    if len(word) == n:
        total += 50

    return total
        

#
# Problem #2: Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,              # print all on the same line
                                        # print an empty line
#
# Problem #2: Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    hand2 = hand.copy()
    #loop through each letter subtracting from key:value
    for letter in word:
        hand2[letter] = hand2[letter] - 1
        
    return hand2
#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    hand2 = hand.copy()
    
    if word not in word_list:
        return False
    
    for letter in word:
        #initial check to see if letter is in hand at all
        if letter not in hand.keys():
            return False
        else:
            #subtract all the values in dictionary, check if any return negative value
            hand2[letter] = hand2[letter] - 1
            if hand2[letter] < 0:
                return False
    return True


#
# Problem #4: Playing a hand
#

def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    handLength = 0

    for letter in hand.keys():
        handLength += hand[letter]

    return handLength


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      
    """
    # Keep track of two numbers: the number of letters left in your hand and the total score
    totalScore = 0
    
    #check if letters are left in the hand
    while calculate_handlen(hand) > 0:    
        # Display the hand
        print "Current Hand:",
        display_hand(hand)
        print
        # Ask user for input
        word = raw_input('''Enter word or a "." to indicate you are finished: ''')
        # If the input is a single period:
        if word == ".":
            break
            # End the game (break out of the loop)
        # Otherwise (the input is not a single period):
        else:
            # If the word is not valid:
            if not is_valid_word(word, hand, word_list):
                # Reject invalid word (print a message)
                print "Please enter a valid word"
                print
            # Otherwise (the word is valid):
            else:
                # Tell the user how many points the word earned, and the updated total score 
                totalScore += get_word_score(word, handsize)
                print '''"%s" earned %d points. Total: %d''' % (word, get_word_score(word, handsize),totalScore)
                print
                # Update hand and show the updated hand to the user
                hand = update_hand(hand, word)

    # Game is over (user entered a '.' or ran out of letters), so tell user the total score
    print "Total score: ", totalScore

#
# Problem #5: Playing a game
# 

def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, ask them again.
 
    2) When done playing the hand, repeat from step 1    
    """
    #generate initial hand
    hand = deal_hand(handsize)
    #generic while loop to keep running until user exits
    test = 1
    while test != 0:
        print
        print "Enter 'n' for new random hand"
        print "Enter 'r' to replay hand"
        print "Enter 'e' to exit game"
        
        userOption = raw_input("Enter option: ")
        
        if userOption == 'n':
            #generates new random hand
            hand = deal_hand(handsize)
            print
            play_hand(hand, word_list)
        elif userOption == 'r':
            print
            play_hand(hand, word_list)
        elif userOption == 'e':
            print "Thank you for playing"
            break
        else: print "Please enter a valid option."
   


#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
