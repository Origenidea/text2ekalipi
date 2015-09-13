#!/usr/bin/python -OO
# -*- coding: utf-8 -*-
import lxml.etree as etree
import operator
import unicodecsv as csv
import re
import sys
import json
import redis

reload(sys)
sys.setdefaultencoding('utf-8')
r = redis.StrictRedis(host='localhost', port=6379, db=0)

eka_map = {}

def load(do_insert=False):
    global eka_map

    if do_insert:
        print "Loading wiki into redis. Wait a few hours..."
        r.flushdb()
        load_wik_table()
        print "Ok Done."
        sys.exit(0)
    
    eka_map = load_eka_table()


def parse_wik(file_name='./ref/enwiktionary.xml', lang_list=[]):
    lang_set = set(lang_list)
    
    # This is the pronounciation regex
    pr_re_english = re.compile(r'{IPA\s*\|\s*-?.?([^|\/\]]+).+lang=\s*(en)')
    pr_re_short = re.compile(r'{{a\|U.}} {{(en)\|([^}]*)}}')
    pr_re = re.compile(r'{IPA\s*\|\s*-?.?([^|\/\]]+).+lang=\s*([\-\w]+)')

    # A number of words have this thing reversed -- "anyone can edit" ...
    pr_re_reversed = re.compile(r'{IPA\|\s*lang=([\-\w]+)\s*\|\s*[\[\/]?([^}\]\|\/]+)')

    # We keep track of how many words we have seen versus how many there are.
    total = 0

    for event, elem in etree.iterparse(file_name, events=('end',), strip_cdata=False, remove_blank_text=True, remove_comments=True, remove_pis=True, encoding='utf-8', huge_tree=True):

        # Get the title of the document (which we may just be ignoring)
        if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}title':
            title = elem.text

        # This checks to see if it's an article about a word
        elif elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}ns':
            flag = (elem.text == '0')

        # This is the text from the article ... we can process
        # it here because we have guarantees on its serialized
        # reading
        elif elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}text' and flag and elem.text:
            text = re.sub(r'enPR', 'en', elem.text)
            #print "QQ",title,"QQ"#, text

            res = pr_re_english.findall(text)

            if len(res) == 0:
                res = pr_re_short.findall(text)
                # need to reverse the mapping
                res = [(t[1], t[0]) for t in res]
                #print "ZZ",res,"ZZ"

            if len(res) == 0:
                res = pr_re.findall(text)

            if len(res) == 0:
                res = pr_re_reversed.findall(text)
                res = [(t[1], t[0]) for t in res]

            if len(res) > 0: 
                # If the language support list is set, then we
                # only have results that are within the supported
                # language set
                if len(lang_set) > 0:
                    res = filter(lambda t: t[1] in lang_set, res)

            if len(res) > 0:
                yield [title, {t[1]: t[0] for t in res}]
            

        # Delete the elements to maintain a flat memory --
        # Without this the memory usage balloons to the multi-gig
        # range
        if elem.getprevious() is not None:
           del elem.getparent()[0]

def load_wik_table():
    ix = 0
    for couple in parse_wik():
        ix += 1
        r.set(couple[0].lower(), json.dumps(couple[1]))

        if ix % 1000 == 0:
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


def wik_to_eka(wik, source_word=None):
    res = ''

    if 'de' in wik: lang = 'de'
    elif 'en' in wik: lang = 'en' 
    else:
        print "Unable to find lang for %s." % (source_word, ), wik
        return None
    
    source = re.sub(r'[\(\)]', '', wik[lang])

    for letter in source:
        if letter in eka_map:
            res += eka_map[letter][lang]
        else:
            print "Unable to find '%s' character for word '%s' (%s)" % (letter, source, source_word)

    return res

def prepare(word):
    return word.lower()

def to_middleware(word):
    exists = r.get(word)

    if exists:
        return json.loads(exists)

    return None

def to_eka(word):
    wik_word = to_middleware(word)

    if wik_word:
        eka_word = wik_to_eka(wik_word, source_word=word)
        return eka_word

    return None

if __name__ == '__main__':
    load_wik_table()
    print parse_file()
