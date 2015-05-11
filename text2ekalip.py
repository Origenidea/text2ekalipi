#!/usr/bin/env python
import re
import sys
import csv

cmu_map = {}
def loadcmu():
    cmu_file = open("ref/cmudict_SPHINX_40", 'rb')

    for line in cmu_file:
        words = re.split(r'\s+', line);
        cmu_map[words[0]] = words[1:-1]

def cmu2ek(word):
    return word

def word2ek(word):
    # The CMU dict is all uppercase so we need that first
    word = word.upper()

    if word in cmu_map:
        return cmu_map[word]
    else:
        return word

loadcmu()

while 1:
    line = sys.stdin.readline()

    # remove numerics.
    line = re.sub(r'\d+', '', line)

    wordlist = re.split(r'[^\w\d]+', line)

    # remove the empty strings
    wordlist = filter(None, wordlist)

    # If this results in a blank line,
    # then we just loop again
    if len(wordlist) == 0:
        continue

    print str(wordlist)

    for word in wordlist:
        cmu = word2ek(word)

        if(len(cmu) == 0):
            cmu = word

        print word + " " + str(cmu)
