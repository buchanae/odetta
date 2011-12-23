import logging

from nose.tools import eq_
import mrjob

from calc_distance_stats import CalcDistanceStats
from combine_splats import CombineSplats
from filter_complete_pair import FilterCompletePair
from filter_invalid_pair import FilterInvalidPair
from split_splat import SplitSplat

import test_files as tf


# disable mrjob loggers
logging.getLogger('mrjob.local').setLevel(100)
logging.getLogger('mrjob.runner').setLevel(100)
logging.getLogger('mrjob.conf').setLevel(100)


def test_split_splat():
    f = open(tf.path('splat'))
    j = SplitSplat().sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(['bas', 'baz', 'foo'], sorted([x[0] for x in out]))

def test_filter_complete_pair():
    f = open(tf.path('filter_complete.sam'))
    j = FilterCompletePair().sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(['BAR\\2', 'OOF\\1'], sorted([x[0] for x in out]))

def test_inverted_filter_complete_pair():
    f = open(tf.path('filter_complete.sam'))
    j = FilterCompletePair(args=['--invert']).sandbox(f)
    j.run_job()
    out = j.parse_output()
    print out
    eq_(['BAS\\1', 'BAS\\2', 'BAZ\\1', 'BAZ\\2', 
         'FOO\\1', 'FOO\\2', 'TEST\\1', 'TEST\\2'], sorted([x[0] for x in out]))

def test_filter_invalid_pairs():
    f = open(tf.path('filter_invalid'))
    j = FilterInvalidPair().sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(['bat', 'bay', 'foo'], sorted([x[0] for x in out]))

def test_filter_invalid_pairs_with_distance():
    f = open(tf.path('filter_invalid_distance'))
    j = FilterInvalidPair(args=['--min-distance', '100', 
                                '--max-distance', '1000']).sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(['bar', 'bas'], sorted([x[0] for x in out]))

def test_combine_splats():
    f = open(tf.path('combine_splats'))
    j = CombineSplats().sandbox(f)
    j.run_job()
    out = j.parse_output(mrjob.protocol.RawValueProtocol())
    eq_(1, len(out))
    eq_('ChrB\tAT-TG\t11\t88\t77\t56\t78\t12\t34\tATCG\t2\tbar,foo\t-1\n', out[0][1])

def test_distance_stats():
    f = open(tf.path('distance_stats'))
    j = CalcDistanceStats().sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(1, len(out))
    eq_([470.0, 455.63142999578071], out[0][1])
