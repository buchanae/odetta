from nose.tools import eq_

from alignment import *


def test_ID_base():
    eq_('foo', ID_base('foo\\1'))
    eq_('foo', ID_base('foo'))

def test_distance_between():
    class Alignment(object):
        def __init__(self, start, end):
            self.start = start
            self.end = end

    a = {'start': 15, 'end': 30}
    b = {'start': 45, 'end': 60}

    eq_(15, distance_between(a, b))
    eq_(15, distance_between(b, a))

def test_SAM():
    a = parse_SAM('foo\\1\t16\tChr1\t15\t0\tCIGAR\t*\t0\t0\tATCG\t*\n')

    eq_('foo\\1', a['ID'])
    eq_('Chr1', a['chromosome'])
    eq_(15, a['start'])
    eq_(19, a['end'])
    eq_('-1', a['strand'])

    b = parse_SAM('foo\\1\t0\tChr1\t15\t0\tCIGAR\t*\t0\t0\tATCG\t*\n')
    eq_('1', b['strand'])

def test_Splat():
    base = 'ChrC\tAT-TT\t10\t99\t55\t1\t2\t3\t4\tGCTA'
    read_data = '2\tbas,baz'
    strand = '-1'
    raw = '\t'.join([base, read_data, strand])
    a = parse_splat(raw)

    eq_('ChrC', a['chromosome'])
    eq_(1, a['start'])
    eq_(4, a['end'])
    eq_(['bas', 'baz'], a['IDs'])
    eq_('-1', a['strand'])
    eq_('\t'.join([base, '{read_count}\t{IDs}', strand]), a['template'])
