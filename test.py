#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
prefix = '{http://www.mediawiki.org/xml/export-0.10/}'

for event, elem in etree.iterparse('./ref/enwiktionary.xml', events=('start', 'end', 'start-ns', 'end-ns')):
    if event == 'start':
        if elem.tag == prefix + 'title':
            print str(elem), elem.text
        elem.clear()

#print event, elem
