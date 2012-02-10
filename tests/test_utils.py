from nose.tools import eq_

from odetta.utils import *


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
