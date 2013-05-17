# 6.00 Problem Set 4
#
# Part 2 - RECURSION
#
# Name          : Jorge Amaya
# Collaborators : None
# Time spent    : 4:00

#
# Problem 3: Recursive String Reversal
#
def reverse_string(string):
    """
    Given a string, recursively returns a reversed copy of the string.
    For example, if the string is 'abc', the function returns 'cba'.
    The only string operations you are allowed to use are indexing,
    slicing, and concatenation.
    
    string: a string
    returns: a reversed string
    """
    if string == "":
        return string

    #Leave last letter in string and do recursive function on remaining letters.
    else:
        return string[-1] + reverse_string(string[:-1])

#
# Problem 4: Srinian
#
def x_ian(x, word):
    """
    Given a string x, returns True if all the letters in x are
    contained in word in the same order as they appear in x.

    >>> x_ian('srini', 'histrionic')
    True
    >>> x_ian('john', 'mahjong')
    False
    >>> x_ian('dina', 'dinosaur')
    True
    >>> x_ian('pangus', 'angus')
    False
    
    x: a string
    word: a string
    returns: True if word is x_ian, False otherwise
    """
    if len(x) > 0 and len(word) > 0:
        
        #If char match, move on to next letters
        if x[0] == word[0]:
            x_ian(x[1:], word[1:])

        #If char don't match increment the word and leave x the same
        else:
            x_ian(x, word[1:])
            
    #If all letters of x are cleared in order, return True
    elif len(x) == 0:
        return True

    else:
        return False
                         

#
# Problem 5: Typewriter
#

def find_space(text, line_length):
    '''
    Given a block of text, returns the first instance of a space (between
    words) that is equal to or greater than initial index value.

    text: a string
    line_length: integer, index value
    returns: integer where space is
    '''
    #if you get to end of string, just returns generic index
    if len(text) <= line_length:
        return line_length
    
    #look for " " between words, returns index value where this occurs
    elif text[line_length] == " ":
        return line_length
            
    #recursion that increments the index value + 1, until it finds " " or reaches end of string
    else:
       return find_space(text, line_length + 1)
   
def insert_newlines(text, line_length):
    """
    Given text and a desired line length, wrap the text as a typewriter would.
    Insert a newline character ("\n") after each word that reaches or exceeds
    the desired line length.

    text: a string containing the text to wrap.
    line_length: the number of characters to include on a line before wrapping
        the next word.
    returns: a string, with newline characters inserted appropriately. 
    """
    #uses helper function to look for the first instance of a " " after the line_length value
    index = find_space(text, line_length)
    
    #for lines that are smaller than the index just return remaining text
    if len(text) <= index:
        return text

    #recursion that returns string up to the index value then runs function on rest of string until out of char
    else:
        return text[:index] + "\n" + insert_newlines(text[index+1:], line_length) 

#f() test
#text = "In practice, Turing completeness means, that the rules followed in sequence on arbitrary data can produce the result of any calculation"
#print insert_newlines(text, 29)


