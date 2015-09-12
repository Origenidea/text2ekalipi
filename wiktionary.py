#!/usr/bin/python -OO
# -*- coding: utf-8 -*-
import unicodecsv as csv
import sys
import json
import redis
import wikparse as pwik

reload(sys)
sys.setdefaultencoding('utf-8')
r = redis.StrictRedis(host='localhost', port=6379, db=0)

def load_wik_table():

    ix = 0
    for couple in pwik.parse_wik():
        ix += 1
        r.set(couple[0], json.dumps(couple[1]))

        if ix % 10000 == 0:
            sys.stderr.write('.')

def load_eka_table(csv_file = 'ref/ipa_kb.csv'):
    csv_handle = open(csv_file, 'rb')

    mapper = {}
    first = True

    for row in csv.reader(csv_handle, encoding='utf-8'):
        if not first:
            ipa, en, de = row[0], row[1], row[6]
            mapper[ipa] = {'en': en, 'de': de}

        first = False

    return mapper

def load():
    eka = load_eka_table()
    pass

def to_eka(word):
    pass


if __name__ == '__main__':
    load_wik_table()
    print parse_file()
