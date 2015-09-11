#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys

def load(file_name="ref/cmu_ekal.txt"):
    ek_file = open(file_name, 'rb')

    ek_map = []
    for line in ek_file:
        words = re.split(r'\s+', line);
        ek_map[words[0]] = words[1]

    return ek_map
