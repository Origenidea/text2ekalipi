#!/usr/bin/python -OO
# -*- coding: utf-8 -*-
import lxml.etree as etree
import operator
import time
import json
import gc
import re
import pprint
import sys

pp = pprint.PrettyPrinter(depth=6)
gc.enable()

# According to the internet, utf-8 is kinda odd, so we have
# to do a bunch of acrobatics to get it working.
reload(sys)
sys.setdefaultencoding('utf-8')

# This is the pronounciation regex
pr_re_english = re.compile(r'{IPA\s*\|\s*-?.?([^|\/\]]+).+lang=\s*(en)')
pr_re = re.compile(r'{IPA\s*\|\s*-?.?([^|\/\]]+).+lang=\s*([\-\w]+)')

# A number of words have this thing reversed -- "anyone can edit" ...
pr_re_reversed = re.compile(r'{IPA\|\s*lang=([\-\w]+)\s*\|\s*[\[\/]?([^}\]\|\/]+)')

# We keep track of how many words we have seen versus how many there are.
ix = 0
total = 0
p_total = 0
count = {'en': 0, 'fr': 0, 'pt': 0, 'ms': 0, 'nrf': 0, 'gd': 0, 'nl': 0, 'da': 0, 'de': 0, 'ro': 0, 'osx': 0, 'fro': 0, 'pl': 0, 'mul': 0, 'eo': 0, 'it': 0, 'lb': 0, 'nn': 0, 'str': 0, 'sco': 0, 'sms': 0, 'so': 0, 'la': 0, 'jbo': 0, 'zza': 0, 'fo': 0, 'liv': 0, 'no': 0, 'sh': 0, 'tk': 0, 'hu': 0, 'ang': 0, 'tl': 0, 'ga': 0, 'oc': 0, 'es': 0, 'ja': 0, 'ca': 0, 'kw': 0, 'vo': 0, 'amm': 0, 'nap': 0, 'sv': 0, 'fy': 0, 'io': 0}

# And how long it takes
start = time.time()

# This is a symlink.
xmlfile = './ref/enwiktionary.xml'

for event, elem in etree.iterparse(xmlfile, events=('end',), strip_cdata=False, remove_blank_text=True, remove_comments=True, remove_pis=True, encoding='utf-8', huge_tree=True):

    # Get the title of the document (which we may just be ignoring)
    if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}title':
        title = elem.text

    # This checks to see if it's an article about a word
    elif elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}ns':
        total += 1
        flag = (elem.text == '0')

    # This is the text from the article ... we can process
    # it here because we have guarantees on its serialized
    # reading
    elif elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}text' and flag and elem.text:
        res = pr_re_english.findall(elem.text)

        if len(res) == 0:
            res = pr_re.findall(elem.text)

        if len(res) == 0:
            res = pr_re_reversed.findall(elem.text)
            res = [(t[1], t[0]) for t in res]

        if len(res) > 0: 

            p_total += len(res)
            # This is a word match, keep track of it.
            ix += 1
            if ix % 10000 == 0:
                now = time.time()
                sys.stderr.write(str(ix) + " " + "{0:.4f}".format( ix / (10 * (now - start)) ))
                sort_count = sorted(count.items(), key=operator.itemgetter(1))
                sort_count = filter(lambda x: x[1] > (ix / 30), sort_count)
                sort_count = map(lambda x: [x[0], "{0:.2f}".format(100.0 * x[1] / ix)], sort_count)
                sys.stderr.write(json.dumps(list(reversed(sort_count))) + "\n")

            seen = {}
            for t in res:
                lang = t[1]

                if lang not in count:
                   count[lang] = 0 

                # Only count this once per word.
                if lang not in seen:
                   seen[lang] = 1
                   count[lang] += 1

            print json.dumps([title,res])
        
        # This debugging provides for checking if a regex is off
        #else:
        #    sys.stderr.write( elem.text )
       

    # Delete the elements to maintain a flat memory --
    # Without this the memory usage balloons to the multi-gig
    # range
    if elem.getprevious() is not None:
       del elem.getparent()[0]

sys.stderr.write(str(ix) + " pronunciations found out of " + str(total) + " documents in " + str((time.time() - start)) + " seconds.\n")
