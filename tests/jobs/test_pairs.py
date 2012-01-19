from nose.tools import eq_, ok_

from jobs.pairs import *
from tests import dummy, disable_mrjob_loggers


disable_mrjob_loggers()


def test_distance_stats():
    f = dummy('distance_stats')
    j = DistanceStatistics().sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(1, len(out))
    eq_([470.0, 455.63142999578071], out[0][1])


def test_ToSplat():
    f = dummy('combine_splats')
    j = ToSplat().sandbox(f)
    j.run_job()
    out = j.parse_output(ToSplat.OUTPUT_PROTOCOL)
    eq_(2, len(out))
    a = '\t'.join(['ChrD', 'AT-GT', '10', '11', '13', '21', '22', '23', '24',
                   'ATCG', '2', 'bay1,bay2', '-'])
    b = '\t'.join(['ChrC', 'AT-GT', '50', '51', '53', '61', '62', '63', '64',
                   'ATTT', '2', 'foo1,foo2', '-'])
    ok_([b, a], sorted([x[1] for x in out]))


def test_ValidFilter():
    f = dummy('filter_invalid')
    j = ValidFilter().sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(['bat', 'bay', 'foo'], sorted([x[0] for x in out]))


def test_ValidFilter_by_distance():
    f = dummy('filter_invalid_distance')
    j = ValidFilter(args=['--min-distance', '100', 
                          '--max-distance', '1000']).sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(['bar', 'bas'], sorted([x[0] for x in out]))


def test_unambiguous_filter():
    f = dummy('unambiguous')
    j = UnambiguousFilter().sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_([('foo\\1', 'foo\\2'), ('foo\\2', 'foo\\1')], 
        sorted([(x[1][0]['ID'], x[1][1]['ID']) for x in out]))


def test_inverted_unambiguous_filter():
    f = dummy('unambiguous')
    j = UnambiguousFilter(args=['--invert']).sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_([('bar\\1', 'bar\\2'), ('bar\\1', 'bar\\2')], 
        sorted([(x[1][0]['ID'], x[1][1]['ID']) for x in out]))


def test_reference_counts():
    f = dummy('reference_counts')
    j = ReferenceCounts().sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(3, len(out))
    d = dict(x for x in out)
    eq_({'one-one': 1, 'one-two': 2}, d['ChrC'])
    eq_({'one-one': 3}, d['ChrD'])
    eq_({'one-one': 1}, d['ChrR'])


def test_combiner():
    f = dummy('combiner')
    j = Combiner().sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_([(1, 3), (2, 3), (5, 6)], sorted([(x[1][0]['n'], x[1][1]['n']) for x in out]))


def test_incomplete_filter():
    f = dummy('incomplete_filter')
    j = IncompleteFilter().sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(['baz\\1'], sorted([x[1]['ID'] for x in out]))


def test_incomplete_filter_inverted():
    f = dummy('incomplete_filter')
    j = IncompleteFilter(args=['--invert']).sandbox(f)
    j.run_job()
    out = j.parse_output()
    eq_(['bar\\1', 'bar\\2', 'foo\\1', 'foo\\2'], sorted([x[1]['ID'] for x in out]))
