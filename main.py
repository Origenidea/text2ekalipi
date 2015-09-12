#!/usr/bin/python -OO
# -*- coding: utf-8 -*-
import re
import sys
import lib.ek as ek
import lib.wik as wik

right = []
wrong = []

ek_map = ek.load()
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
    ek_real = wordlist[1]

    word = wordlist[0]
    # This is our generated set
    ek_test = word2ek(word)
    cmu_test = ' '.join(word2cmu(word))

    if ek_test == ek_real:
        right.append([word, cmu_test, ek_real, ek_test])
    else:
        wrong.append([word, ek_real, ek_test, cmu_test])

    total += 1

print "Results: " + str( 100 * len(right) / total) + "% correct"
print "Wrong List:"

for line in wrong:
    print "\t".join(line)

print "\n\n\nRight List:"
for line in right:
    print "\t".join(line)
