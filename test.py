#!/usr/bin/python -O
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
pr_re = re.compile('{{IPA\|.?([^|\/]*).+lang=en}}', re.M | re.U)

flag = False 
text = None

tag_title = prefix + 'title'
tag_text = prefix + 'text'
tag_ns = prefix + 'ns'
tag_page = prefix + 'page'
ix = 0
start = time.time()
xmlfile = './ref/enwiktionary.xml'


"""
def fast_iter(context, func, *args, **kwargs):
    http://lxml.de/parsing.html#modifying-the-tree
    Based on Liza Daly's fast_iter
    http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    See also http://effbot.org/zone/element-iterparse.htm
    for event, elem in context:
        func(elem, *args, **kwargs)
        # It's safe to call clear() here because no descendants will be
        # accessed
        elem.clear()
        # Also eliminate now-empty references from the root node to elem
        for ancestor in elem.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
    del context


def process_element(elem):
    print elem.xpath( 'description/text( )' )

context = etree.iterparse( xmlfile, tag='' )
fast_iter(context,process_element)
"""

for event, elem in etree.iterparse(xmlfile, events=('start', 'end')):
    ix += 1
    if ix % 100000 == 0:
        gc.collect()
        now = time.time()
        sys.stderr.write(str( ix / (now - start) ) + "\n")

    if event == 'start':
        if elem.tag == tag_title:
            title = elem.text
        elif elem.tag == tag_ns and elem.text == '0':
            flag = True
        elif elem.tag == tag_text and flag:
            text = elem.text
        elem.clear()

    elif event == 'end':
        if elem.tag == tag_page:
            if flag and text and title:
                res = pr_re.search(text)
                if res: 
                    print title.decode('utf-8') + ',' + res.group(1).decode('utf-8')

            flag = False
            title = None
            text = None
        elem.clear()

        while elem.getprevious() is not None:
             del elem.getparent()[0]
    """
    for ancestor in elem.xpath('ancestor-or-self::*'):
        while ancestor.getprevious() is not None:
            del ancestor.getparent()[0]
    """

