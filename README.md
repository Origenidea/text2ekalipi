# text2ekalipi

This is an english text to [ekalipi](www.ekalipi.org) translator using the CMU Sphinx library.

There's also experiments with the [wiktionary ipa](https://dumps.wikimedia.org/enwiktionary) which which expanded to 3.5GB.  Because of that, it's not included in the repository and can be grabbed and set up using `ref/grab-wiktionary.sh`.

The output of `parse-wiktionary.py` uses python's itertools parser in the lxml library and takes effort to be a flat-memory implementation. At least on *my* system it grows to about 14MB resident and then holds out there.  Parsing through all of wiktionary takes about 180s and a sorted output of a snapshot of the wiktionary xml (with 325.6k words) is presented in an lzma file in `ref/wiktionary-20150413-sorted.txt.lzma`
