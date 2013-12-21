#!/usr/bin/env python

import random

def get_from_database():
    return [random.choice('ABCDEFGH') for _ in xrange(random.randint(1, 5))]

def pair():
    return (frozenset(get_from_database()), frozenset(get_from_database()))

set_of_tuples = set(pair() for _ in xrange(7))
set_of_tuples.add((frozenset(['A', 'B']), frozenset(['X'])))
print set_of_tuples
