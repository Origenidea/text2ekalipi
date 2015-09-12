#!/usr/bin/python -OO
# -*- coding: utf-8 -*-
import re
import sys
import lib.ek as ek
import lib.cmu as cmu
import lib.wik as wik

engine = wik
engine.load()

right = []
wrong = []

total = 0
for line in sys.stdin:

    wordlist = re.split(r'\s+', line)

    # remove the empty strings
    wordlist = filter(None, wordlist)

    # If this results in a blank line,
    # then we just loop again
    if len(wordlist) < 2:
        continue

    # This is the reference set
    eka_real = wordlist[1]
    word = wordlist[0]

    # This is our generated set
    eka_test = engine.to_eka(word)
    engine_test = ' '.join(word2cmu(word))

    if ek_test == ek_real:
        right.append([word, engine_test, eka_real, eka_test])
    else:
        wrong.append([word, eka_real, eka_test, engine_test])

    total += 1

print "Results: " + str( 100 * len(right) / total) + "% correct"
print "Wrong List:"

for line in wrong:
    print "\t".join(line)

print "\n\n\nRight List:"
for line in right:
    print "\t".join(line)
