#!/usr/bin/env python
import re
import sys
import csv

cmu_map = {}
ek_map = {}

def loadek():
    ek_file = open("ref/cmu_ekal.txt", 'rb')

    for line in ek_file:
        words = re.split(r'\s+', line);
        ek_map[words[0]] = words[1]

def loadcmu():
    cmu_file = open("ref/cmudict_SPHINX_40", 'rb')

    for line in cmu_file:
        words = re.split(r'\s+', line);
        cmu_map[words[0]] = words[1:-1]

def cmu2ek(cmu):
    ek = []

    for pho in cmu:
        if pho in ek_map:
            ek.append(ek_map[pho])
        else:
            ek.append("MISSING")

    return ek

def word2cmu(word):
    # The CMU dict is all uppercase so we need that first
    word = word.upper()

    if word in cmu_map:
        return cmu_map[word]
    else:
        return word

def word2ek(word):
    cmu = word2cmu(word)
    # This means that the CMU dict didn't
    # have the word to begin with
    if type(cmu) is str:
        return "MISSING"

    # This always returns a list
    ek = cmu2ek(cmu)
    return ''.join(ek)

def transline(line):
    # remove numerics.
    line = re.sub(r'[\d_]+', '', line)

    wordlist = re.split(r'[^\w]+', line)

    # remove the empty strings
    wordlist = filter(None, wordlist)

    # If this results in a blank line,
    # then we just loop again
    if len(wordlist) == 0:
        continue

    for word in wordlist:
        cmu = word2cmu(word)

        # This means that we couldn't find
        # this word in the CMU dict.
        if type(cmu) is str:
            print word + " " + str(cmu)

        else:
            ek = cmu2ek(cmu)
            print ''.join(ek)

loadcmu()
loadek()

while 1:
    line = sys.stdin.readline()

    # remove numerics.
    line = re.sub(r'[\d_]+', '', line)

    wordlist = re.split(r'[^\w]+', line)

    # remove the empty strings
    wordlist = filter(None, wordlist)

    # If this results in a blank line,
    # then we just loop again
    if len(wordlist) == 0:
        continue

    word2cmu(
    for word in wordlist:
        cmu = word2cmu(word)

        # This means that we couldn't find
        # this word in the CMU dict.
        if type(cmu) is str:
            print word + " " + str(cmu)

        else:
            ek = cmu2ek(cmu)
            print ''.join(ek)
