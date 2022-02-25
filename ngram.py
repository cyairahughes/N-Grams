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


import re
import sys
import random

#dictionary that stores ngrams of length n and their count
dictN = {}
#dictionary that stores ngrams of length n-1 and their count
dictNMin1 = {}
#dictionary that stores ngrams of length 1 and their count
dictUni = {}
#dictionary that stores ngrams of length n and their relative frequency
dictFreqs = {}


def main():
    #how I chose to represent start and end tags
    startTag = "<start>"
    endTag = "<end>"
    #gets the number of elements in the command line
    lengthOfArgs = len(sys.argv)
    #stores n given in command line
    n = int(sys.argv[1])
    #stores m given in command line
    m = int(sys.argv[2])
    #list to store files given in commandline
    files = []
    #initializes corpus
    corpus = ''
    #prints out what the program is going to do and what was input from command line
    print('\nThis program generates random sentences based on an Ngram model. \n'
          'Command line settings : ' + sys.argv[0] + ' ' + str(n) + ' ' + str(m) + '\n')
    #adds each file given to file list
    for i in range(3, lengthOfArgs):
        files.append(sys.argv[i])
    #every word in each file is added to corpus after preprocessing
    for i in range(0, len(files)):
        corpus = corpus + preprocess(files[i], n, startTag, endTag)
    #split corpus into tokens and add to words list
    words = corpus.split()
    #adds words and counts to dictN, given n
    addToDict(words,n, dictN)
    #adds words and counts to dictNMin1, given n
    addToDict(words,n-1, dictNMin1)
    #adds words and counts to dictUni, given n
    addToDict(words,1, dictUni)
    #add words and relative frequencies to dictFreq, given n
    calcFreq(words, n)
    #if n is 1 use generate method to generate m sentences
    if n == 1:
        for i in range(m):
            generate(n)
    #else use generateN method to generate m sentences
    else:
        for i in range(m):
            generateN(n)

def preprocess(file, n, startTag, endTag):
    st = startTag
    #duplicates start tag n-1 times seperated by spaces
    for i in range(1, n - 1):
        startTag = startTag + ' ' + st
    #opens file and replaces format errors with '?'
    f = open(file, 'r', errors='replace')
    #copies file into string
    text = f.read()
    #closes file
    f.close()
    #converts all chars in string to lowercase
    text = text.lower()
    #substitues nonwords, nonspaces, and non['.','?','!'] with empty space
    text = re.sub(r"[^\w\s\.!\?]", '', text)
    #supstitutes all ['.','?','!'] with an end tag follwed by a start tag, sparated by spaces
    #text = re.sub(r'[\.\?!]', ' ' + endTag + ' ' + startTag + ' ', text)
    text = re.sub(r'[\.]', ' . ' + endTag + ' ' + startTag + ' ', text)
    text = re.sub(r'[\?]', ' ? ' + endTag + ' ' + startTag + ' ', text)
    text = re.sub(r'[!]', ' ! ' + endTag + ' ' + startTag + ' ', text)
    #adds start tag to beginning of text seperated by space
    corpus = startTag + ' ' + text
    #replaces tabs and newlines with spaces
    corpus = corpus.replace('\r', ' ').replace('\n', ' ')
    #return text
    return corpus


def addToDict(words, n, dict):
    #initialize list
    list = []
    #iterates through every word in list, len-n+1 to account for trailing words that do not fit in ngram
    for i in range(len(words) - n + 1):
        #store k as i
        k = i
        #add n words to list starting at i
        for j in range(n):
            list.append(words[k])
            k = k + 1
        #if words are already found in list increase count by 1
        if tuple(list.copy()) in dict:
            dict[tuple(list.copy())] += 1
        #if words are not found in list initialize count to 1
        if tuple(list.copy()) not in dict:
            dict[tuple(list.copy())] = 1
        #clear list after every iteration
        list.clear()


def calcFreq(corpus, n):
    #if n is greater than 1
    if n > 1:
        #iterate through all keys in dictN
        for key in dictN:
            #intitialize list
            l = []
            #add ith element in key to list n-1 times
            for i in range(n-1):
                l.append(key[i])
            #stores frequency of word(s)1
            w1 = dictNMin1[tuple(l)]
            #stores frequency word(s) 1 and 2
            w1w2 = dictN[key]
            #clear list
            l.clear()
            #add key to dictFreq and P(w2|w1)
            dictFreqs.update({key : w1w2 / w1})
    #if n is 1
    else:
        #iterate through all keys in dictUni
        for key in dictUni:
            #add key to dictFreq and P(word|corpus)
            dictFreqs.update({key : dictUni[key] / len(corpus)})


def generate(n):
    #word is stored as start tag
    word = ''.join(list(dictFreqs.keys())[0])
    #initialize sentence string
    sentence = ''
    #initialize words list
    words = []
    #initilize variable to false because sentence words are length 0
    isAppropriateLen = False
    #iterate through keys in dictFreq while word is not end tag and length of words is not >= n
    #while word != '<end>' or isAppropriateLen == False:
    while not (word.__contains__('.') or word.__contains__('?') or word.__contains__('!') ) or len(words) < n:
        #store count as float 0.0
        count = 0.0
        #generate random number
        rand = random.random()
        #iterate through keys in dictFreq
        for key in dictFreqs:
            #add frequency of key to count
            count += dictFreqs[key]
            #if count is greater than or equal to random number
            if count >= rand:
                #store word as key
                word = ''.join(key)
                #break out of loop
                break
        #if the word is not the end or start tag
        if word != '<end>' and word != '<start>':
            #add word to list
            words.append(word)
            #add word to sentence
            if word == '.' or word ==  '!' or word == '?':

                sentence = sentence + word
            else:
                sentence = sentence + ' ' + word
    print(sentence + '\n')


def generateN(n):
    #initialize listn as list
    listn = []
    #add n-1 start tags to list
    for i in range(n-1):
        listn.append(list(dictFreqs.keys())[0][i])
    #store history as tuple of n-1 start tags
    history = tuple(listn)
    #initialize sentence
    sentence = ''
    #initialize words list
    words = []
    #initialize newDict dictionary
    newDict = ({})
    #while end tag not in history tuple or length of words list is less than n
    while '<end>' not in history or len(words) < n:
        #iterate through keys in dictNMin1
        for keyNMin1 in dictNMin1:
            #if key matches history
            if keyNMin1 == history:
                #iterate through keys in dictFreq
                for freqKey in dictFreqs:
                    #store counter as 0
                    counter = 0
                    #from i to n-1
                    for i in range(n-1):
                        #if element i in key of dictNMin1 == element i in key of dictFreq counter++
                        if keyNMin1[i] == freqKey[i]:
                            counter += 1
                    #if counter == n-1 add dictFreq element to newDict
                    if counter == n-1:
                        newDict.update({freqKey : dictFreqs[freqKey]})
                #generate random number
                rand = random.random()
                #store count as 0
                count = 0
                #iterate through keys in newDict
                for newKey in newDict:
                    #add freqency of key to count
                    count += newDict[newKey]
                    #if count is greater than or equal to random number
                    if count >= rand:
                        #initialize l list
                        l = []
                        #pop off first element in key and add remainder of key to list
                        for i in range(1, n):
                            l.append(newKey[i])
                        #store history as list
                        history = tuple(l)
                        #break out of loop
                        break
                #clear newDict
                newDict.clear()
                #if last word in history is not start or end tag
                if '<end>' != history[n-2] and '<start>' != history[n-2]:
                    #add history to list
                    words.append(history)
                    #add last word to sentence
                    if ''.join(history[len(history)-1]) == '.' or ''.join(history[len(history)-1]) == '!' or ''.join(history[len(history)-1]) == '?':
                        sentence = sentence + ''.join(history[len(history)-1])
                    else:
                        sentence = sentence + ' ' + ''.join(history[len(history)-1])
    #print sentence
    print(sentence + '\n')

#calls main method first
if __name__ == "__main__":
    main()
