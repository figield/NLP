#!/usr/bin/env python

statystyka = set([
    ('glupia', 'koza'),
    ('stara', 'pizda'),
    ('ide', 'do'),
    ('jestem', 'na'),
])


def pary(zdanie): # malo idiomatyczne, ale chyba szybsze, niz zip
    for i in range(1, len(zdanie)):
        yield zdanie[i-1], zdanie[i]

def pary2(zdanie): # ladniej, wolniej(?) zbenchmarkuj sobie
    return zip(zdanie[:-1], zdanie[1:])

if __name__ == '__main__':
    zdanie = 'jestem na zakupach powiedziala stara pizda'.split()
    for a, b in (para for para in pary(zdanie) if para in statystyka):
        print '+', a, b
