#!/usr/bin/python -OO
# -*- coding: utf-8 -*-
import argparse
import re
import sys
import lib.ek as ek
import lib.cmu as cmu
import lib.wik as wik

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--rebuild', action='store_true', help='rebuild databases')
args = parser.parse_args()

engine = wik
engine.load(do_insert=args.rebuild)

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
    word = engine.prepare(wordlist[0])

    # This is our generated set
    eka_test = engine.to_eka(word)
    engine_test = engine.to_middleware(word).values()[0] if eka_test else ''

    if eka_test == eka_real:
        right.append([word, engine_test, eka_real, eka_test])
    else:
        if not eka_test: eka_test = ''
        wrong.append([word, engine_test, eka_real, eka_test])

    total += 1

print "Results: " + str( 100 * len(right) / total) + "% correct"
print "Wrong List:"

for line in wrong:
    print ''.join(['{:20}'.format(x) for x in line])

print "\n\n\nRight List:"
for line in right:
    print ''.join(['{:20}'.format(x) for x in line])
