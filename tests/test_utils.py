from nose.tools import eq_

from odetta.utils import *


def test_parse_ID():

    eq_({
        'instrument': 'SOLEXA1_0001',
        'lane': '7',
        'tile': '1',
        'x': '4',
        'y': '1676',
        'index': '0',
        'pair_member': '1',
        'extra': None,
    }, parse_ID('SOLEXA1_0001:7:1:4:1676#0/1'))

    eq_({
        'instrument': 'SOLEXA1_0001',
        'lane': '7',
        'tile': '1',
        'x': '4',
        'y': '1676',
        'index': None,
        'pair_member': None,
        'extra': None,
    }, parse_ID('SOLEXA1_0001:7:1:4:1676'))

    eq_({
        'instrument': 'HWI-EAS431_0038',
        'lane': '1',
        'tile': '1',
        'x': '1095',
        'y': '10721',
        'index': '0',
        'pair_member': '1',
        'extra': 'BC:ACGT,eeee blah,bar',
    }, parse_ID('HWI-EAS431_0038:1:1:1095:10721#0/1 BC:ACGT,eeee blah,bar'))

    eq_({
        'instrument': 'HWI-ST609',
        'run': '81',
        'flowcell': 'B09K8ABXX',
        'lane': '5',
        'tile': '1101',
        'x': '15096',
        'y': '3548',
        'pair_member': '1',
    }, parse_ID('HWI-ST609:81:B09K8ABXX:5:1101:15096:3548\\1'))


def test_pair_key():

    eq_('7:1:4:1676', pair_key('SOLEXA1_0001:7:1:4:1676#0/1'))
    eq_('5:1101:15096:3548', pair_key('HWI-ST609:81:B09K8ABXX:5:1101:15096:3548\\1'))


def test_distance_between():
    class Alignment(object):
        def __init__(self, start, end):
            self.start = start
            self.end = end

    a = {'start': 15, 'end': 30}
    b = {'start': 45, 'end': 60}

    eq_(15, distance_between(a, b))
    eq_(15, distance_between(b, a))

    a = {'start': 15, 'end': 45}
    b = {'start': 30, 'end': 60}

    eq_(-15, distance_between(a, b))
    eq_(-15, distance_between(b, a))


def test_model_parser():
    m = model_parser([
      ('one', ''),
      ('two', 0),
      ('three', 'd'),
    ])

    b = m(['foo', '1'])
    eq_('foo', b['one'])
    eq_(1, b['two'])
    eq_('d', b['three'])
