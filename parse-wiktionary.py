#!/usr/bin/python -OO
# -*- coding: utf-8 -*-
import lxml.etree as etree
import time
import gc
import re
import sys

# According to the internet, utf-8 is kinda odd, so we have
# to do a bunch of acrobatics to get it working.
reload(sys)
sys.setdefaultencoding('utf-8')
gc.enable()

# This is the pronounciation regex
pr_re = re.compile('{IPA\s*\|\s*.?([^|\/]*).+lang=\s*([\-\w]+)\s*}', re.M | re.U)

# A number of words have this thing reversed -- "anyone can edit" ...
pr_re_reversed = re.compile('{IPA\|\s*lang=([\-\w]+).{1,2}([^}\]|\/]*)[\]\|}]', re.M | re.U)

# Apparently you can't tell lxml to ignore namespaces so we 
# construct things here.
ix = 0
total = 0
start = time.time()
xmlfile = './ref/enwiktionary.xml'

for event, elem in etree.iterparse(xmlfile, events=('end',), tag=None, strip_cdata=False, remove_blank_text=True, remove_comments=True, remove_pis=True, encoding='utf-8', huge_tree=True):

    ## Get the title of the document (which we may just be ignoring)
    if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}title':
        title = elem.text

    ## This checks to see if it's an article about a word
    elif elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}ns':
        total += 1
        flag = (elem.text == '0')

    ## This is the text from the article ... we can process
    ## it here because we have guarantees on its serialized
    ## reading
    elif elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}text' and flag and elem.text:
        res = pr_re.search(elem.text)

        if res:
            matches = res.groups()
            
        else:
            res = pr_re_reversed.search(elem.text)
            if res:
                matches = reversed(res.groups())     

        if res: 

            ## This is a word match, keep track of it.
            ix += 1
            if ix % 10000 == 0:
                now = time.time()
                sys.stderr.write(str(ix) + " " + str( ix / (10 * (now - start)) ) + "\n")

            print title + ',' + (','.join(matches))
        
        #else:
        #    sys.stderr.write( elem.text )
       

    ## Delete the elements to maintain a flat memory --
    ## Without this the memory usage balloons to the multi-gig
    ## range
    if elem.getprevious() is not None:
       del elem.getparent()[0]

sys.stderr.write(str(ix) + " pronunciations found out of " + str(total) + " documents in " + str((time.time() - start)) + " seconds.\n")
