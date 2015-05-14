#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
import re

prefix = '{http://www.mediawiki.org/xml/export-0.10/}'
pr_re = re.compile('{{IPA\|.?([^|\/]*).+lang=en}}', re.M | re.U)

flag = 0
text = False


def getpronounce(text):
    res = pr_re.search(text)
    if res: 
        return res.group(1)
    return res

for event, elem in etree.iterparse('./ref/enwiktionary.xml', events=('start', 'end', 'start-ns', 'end-ns')):
    if event == 'start':
        if elem.tag == prefix + 'title':
            title = elem.text
        elif elem.tag == prefix + 'text' and flag == 1:
            text = elem.text
        elif elem.tag == prefix + 'ns' and elem.text == '0':
            flag = 1
        elem.clear()

    elif event == 'end' and elem.tag == prefix + 'page':
        if flag == 1 and text != None and title != False:
            res = getpronounce(text.encode('utf-8'))
            if res != None:
                print title,res
            #print title,text.encode('utf-8')
        flag = 0
        title = False
        text = False

#print event, elem
