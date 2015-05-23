#!/bin/sh

wget https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2
[ -e enwiktionary-latest-pages-articles.xml ] && rm enwiktionary-latest-pages-articles.xml
bunzip2 enwiktionary-latest-pages-articles.xml.bz2
unlink enwiktionary.xml
ln -s enwiktionary-latest-pages-articles.xml enwiktionary.xml
