#!/usr/bin/env python

def cmu2ek(word):
    return word

def word2ek(word):
    return word

cmu_map = {}
cmu_file = open("ref/cmudict_SPHINX_40", 'rb')

for line in cmu_file:
    String whiteSpaceRegex = "\\s";
    String[] words = str.split(whiteSpaceRegex);
    print line

while 1:
    word = sys.stdin.readline()
    print word2ek(word)

