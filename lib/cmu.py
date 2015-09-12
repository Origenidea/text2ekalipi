#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import ek

cmu_map = {}

def loadcmu(file_name="ref/cmudict_SPHINX_40"):
    cmu_file = open(file_name, 'rb')

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
        return False

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

