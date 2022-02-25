# Cyaira Hughes CMSC416 2/20/22

# URLs used: https://www.w3schools.com/python/python_regex.asp
#            https://www.gutenberg.org
#            https://www.geeksforgeeks.org

# The purpose of this project is to design a program that will
# learn an N-gram language model from an arbitrary number of plain text
# files and generate a given number of sentences based
# on that N-gram model.

# How to run:
#    1. Download file
#    2. Find file in command prompt
#    3. Type "python ngram.py n m ["file_1.txt"] ..["file_k.txt"]" to run program

# Sample Output:
# python ngram.py 3 5 SorcerersStone.txt ChamberOfSecrets.txt
#
# This program generates random sentences based on an Ngram model.
# Command line settings : ngram.py 3 5
#
#  such a scene of the most important ball of the hut was full of turkey and cake and with a trunk he could.
#
#  said hagrid casually he wouldn!
#
#  hes lost his powers sir!
#
#  somewhere over there said griphook.
#
#  selling? percy said as they heaved norbert up the tunnel floor.
# Algorithm:
    # 1. Store m, n and txt files in variables
    # 2. Preprocess each file by first duplicating start tag n-1 times,then read file to corpus and convert to lower
    #    case, remove chars that are not words, spaces, periods,question marks or exclamation points. Convert periods,
    #    question marks, and exclamation points to end tags followed by start tags. Convert tabs or new lines to spaces.
    # 3. Split corpus by spaces and store tokens in list.
    # 4. Add tokens to Ngram dictionary, ignoring repeats and storing their counts.
    # 5. Add tokens to N-1gram dictionary, ignoring repeats and storing their counts.
    # 6. Add tokens to Unigram dictionary, ignoring repeats and storing their counts.
    # 7. If n > 1:
    #            Calculate the probability of a word given the history of a set of words and add to frequency dictionary
    #            for each word in Ngram dictionary.
    #    Else:
    #            Calculate probability of a word given all words in corpus for each word in Unigram.
    # 8. If n == 0:
    #             Generate m sentences by word probability and random number to add variety.
    #    Else:
    #             Generate m sentences by word probability given history and random number to add variety.
