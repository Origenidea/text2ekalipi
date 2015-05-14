#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
prefix = '{http://www.mediawiki.org/xml/export-0.10/}'

for event, elem in etree.iterparse('./ref/enwiktionary.xml', events=('start', 'end', 'start-ns', 'end-ns')):
    if event == 'start':
        if elem.tag == prefix + 'title':
            title = elem.text
        elif elem.tag == prefix + 'ns' and elem.text == '0':
            flag = 1
        elem.clear()

    elif event == 'end' and elem.tag == prefix + 'page':
        if flag == 1:
            print title
        flag = 0

#print event, elem
