#!/usr/bin/env python
import re
import sys

def cmu2ek(word):
    return word

def word2ek(word):
    # The CMU dict is all uppercase so we need that first
    word = word.upper()

    if word in cmu_map:
        return cmu_map[word]
    else:
        return word

cmu_map = {}
cmu_file = open("ref/cmudict_SPHINX_40", 'rb')

for line in cmu_file:
    words = re.split(r'\s+', line);
    cmu_map[words[0]] = words[1:]

while 1:
    line = sys.stdin.readline()
    wordlist = re.split(r'[^\w]+', line)

    for word in wordlist:
        cmu = word2ek(word)

        if(len(cmu) == 0):
            cmu = word

        print str(cmu)
