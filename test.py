#!/usr/bin/python -OO
# -*- coding: utf-8 -*-
import lxml.etree as etree
import time
import gc
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
gc.enable()

prefix = '{http://www.mediawiki.org/xml/export-0.10/}'
pr_re = re.compile('{{IPA\|.?([^|\/]*).+lang=(..)}}', re.M | re.U)

flag = False 
text = None

tag_title = prefix + 'title'
tag_text = prefix + 'text'
tag_ns = prefix + 'ns'
tag_page = prefix + 'page'
ix = 0
start = time.time()
xmlfile = './ref/enwiktionary.xml'

for event, elem in etree.iterparse(xmlfile, events=('end',)):
    if elem.tag == tag_title:
        title = elem.text
    elif elem.tag == tag_ns and elem.text == '0':
        flag = True
    elif elem.tag == tag_text and flag:
        text = elem.text
    elif elem.tag == tag_page:
        if flag and text and title:
            ix += 1
            if ix % 10000 == 0:
                now = time.time()
                sys.stderr.write(str( ix / (1000 * (now - start)) ) + "\n")

            res = pr_re.search(text)
            if res: 
                print title.decode('utf-8') + ',' + (','.join(res.groups())).decode('utf-8')
            """
            else:
                sys.stderr.write( text )
            """

        flag = False
        title = None
        text = None

    elem.clear()

    while elem.getprevious() is not None:
         del elem.getparent()[0]
