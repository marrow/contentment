# encoding: utf-8

import re


minimum = 2
particles = u"""a an the to ah hi oh so as yet as too and or nor but while for was is it will if id has go via can ll"""
particles = dict((i, None) for i in particles.split()) # in checks are faster against dicts than lists

replaced = re.compile(r"(\W|('s))+")


def strip(value):
    values = []
    value = replaced.sub(' ', value)
    
    for i in value.split():
        stripped = i.lower().strip()
        if len(stripped) < minimum or stripped in particles: continue
        values.append(stripped)
    
    return values
    