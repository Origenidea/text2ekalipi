# text2ekalipi

This is an english text to [ekalipi](www.ekalipi.org) translator using the a number of different engines which have different data sources.

The two here are wikitionary (en, de) and the CMU Sphinx. 
are structured

The wiktionary system uses redis because the database is a giant xml file that takes a long time to parse

Each engine should follow the interface outlined below, in order to be interchangable.

## Engine API interface

All engines have a number of functions defined:

### engine.load()
Loads all the tables of the engine and optionally can do any type of large pre-processing and comprehension of documents.

### engine.prepare(word)
Prepares a word to be ingested.  This does things like removal of say, apostrophes, and case substitution so that a dictionary will
be able to find the word

### engine.to_eka(prepared word)
Goes from English to the ekalipi candidate

### engine.to_middleware(prepared word)
Usually engines work off of referential IPA or TTS systems.  They act as a middleware between the source prepared word and the destination ekalipi candidate.  This outputs the middleware word that was considered for introspection.

### old stuff
There's also experiments with the [wiktionary ipa](https://dumps.wikimedia.org/enwiktionary) which which expanded to 3.5GB.  Because of that, it's not included in the repository and can be grabbed and set up using `ref/grab-wiktionary.sh`.

The output of `parse-wiktionary.py` uses python's itertools parser in the lxml library and takes effort to be a flat-memory implementation. At least on *my* system it grows to about 14MB resident and then holds out there.  Parsing through all of wiktionary takes about 180s and a sorted output of a snapshot of the wiktionary xml (with 325.6k words) is presented in an lzma file in `ref/wiktionary-20150413-sorted.txt.lzma`
Each engine has an interface

