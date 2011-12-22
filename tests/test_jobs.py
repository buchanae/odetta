from nose.tools import eq_
from mrjob.protocol import RawValueProtocol

from combine_splats import CombineSplats
from filter_complete_pair import FilterCompletePair
from filter_invalid_pair import FilterInvalidPair
from split_splat import SplitSplat

import test_files as tf


def test_split_splat():
    f = open(tf.path('splat'))
    j = SplitSplat().sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(3, len(out))
    eq_(['bas', 'baz', 'foo'], sorted([x[0] for x in out]))

def test_filter_complete_pair():
    f = open(tf.path('filter_complete.sam'))
    j = FilterCompletePair().sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(2, len(out))
    eq_(['BAR\\2', 'OOF\\1'], sorted([x[0] for x in out]))

def test_filter_invalid_pairs():
    f = open(tf.path('filter_invalid'))
    j = FilterInvalidPair().sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(1, len(out))
    eq_(['foo'], [x[1] for x in out])

def test_combine_splats():
    f = open(tf.path('combine_splats'))
    j = CombineSplats().sandbox(f)
    j.run_job()
    out = j.parse_output(RawValueProtocol())
    eq_(1, len(out))
    eq_('ChrB\tAT-TG\t11\t88\t77\t56\t78\t12\t34\tATCG\t2\tbar,foo\t-1\n', out[0][1])
