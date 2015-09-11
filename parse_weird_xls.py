#!/usr/bin/python -OO
# -*- coding: utf-8 -*-
import unicodecsv as csv
import sys
import gc

reload(sys)
sys.setdefaultencoding('utf-8')
gc.enable()

def parse_file(csv_file = 'ref/ipa_kb.csv'):
    csv_handle = open(csv_file, 'rb')

    mapper = {}
    first = True
    for row in csv.reader(csv_handle, encoding='utf-8'):
        if not first:
            ipa, en, de = row[0], row[1], row[6]
            mapper[ipa] = {'en': en, 'de': de}

        first = False

    return mapper

if __name__ == '__main__':
    print parse_file()
