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
pr_re = re.compile('{IPA\|.?([^|\/]*).+lang=([\-\w]+)}', re.M | re.U)

# A number of words have this thing reversed -- "anyone can edit" ...
pr_re_reversed = re.compile('{IPA\|lang=([\-\w]+).{1,2}([^|\/]*)[\|}]', re.M | re.U)

flag = False 
text = None

# Apparently you can't tell lxml to ignore namespaces so we 
# construct things here.
prefix = '{http://www.mediawiki.org/xml/export-0.10/}'
tag_title = prefix + 'title'
tag_text = prefix + 'text'
tag_ns = prefix + 'ns'
tag_page = prefix + 'page'
ix = 0
start = time.time()
xmlfile = './ref/enwiktionary.xml'

for event, elem in etree.iterparse(xmlfile, events=('end',)):

    ## Get the title of the document (which we may just be ignoring)
    if elem.tag == tag_title:
        title = elem.text

    ## This checks to see if it's an article about a word
    elif elem.tag == tag_ns and elem.text == '0':
        flag = True

    ## This is the text from the article ... we can process
    ## it here because we have guarantees on its serialized
    ## reading
    elif elem.tag == tag_text and flag and title:
        res = pr_re.search(elem.text)

        if res:
            matches = res.groups()
            
        if not res:
            res = pr_re_reversed.search(elem.text)
            if res:
                matches = reversed(res.groups())     

        if res: 

            ## This is a word match, keep track of it.
            ix += 1
            if ix % 1000 == 0:
                now = time.time()
                sys.stderr.write(str(ix) + " " + str( ix / (1000 * (now - start)) ) + "\n")

            print title.decode('utf-8') + ',' + (','.join(matches)).decode('utf-8')
        
        else:
            sys.stderr.write( elem.text )
       

    ## Reset all the flags and variables after each page.
    elif elem.tag == tag_page:
        flag = False

        if title:
            del title

        if text:
            del text

    ## and delete the elements to maintain a flat memory
    elem.clear()

    while elem.getprevious() is not None:
         del elem.getparent()[0]
