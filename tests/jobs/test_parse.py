from nose.tools import eq_, ok_

from odetta.jobs.parse import *
from tests import *


disable_mrjob_loggers()


#TODO test SAM with many extra columns

@dummytest(SAM(), 'sam')
def test_SAM(out):
    out = dict((x[1]['ID'], x) for x in out)

    eq_(3, len(out))

    k, v = out['foo']
    eq_('foo', v['ID'])
    eq_('Chr1', v['reference'])
    eq_(15, v['start'])
    eq_(19, v['end'])
    eq_('-', v['strand'])
    eq_('SAM', v['type'])

    k, v = out['bar']
    eq_('+', v['strand'])


@dummytest(SAM(args=['--type', 'blah']), 'sam')
def test_SAM_type(out):
    k, v = out[0]
    eq_('blah', v['type'])


@dummytest(Splat(), 'splat')
def test_Splat(out):
    out = dict((x[1]['reference'], x) for x in out)

    eq_(3, len(out))

    k, v = out['ChrC']
    eq_(None, k)
    eq_('ChrC', v['reference'])
    eq_(1, v['start'])
    eq_(4, v['end'])
    eq_('-bas,+baz', v['read_IDs'])

    k, v = out['ChrB']

    k, v = out['ChrA']
    eq_('', v['read_IDs'])

@dummytest(SplitSplat(), 'splat')
def test_SplitSplat(out):
    out = dict((x[1]['ID'], x[1]) for x in out)
    eq_(['', 'bas', 'baz', 'foo'], sorted(out.keys()))

    print out
    eq_('-', out['bas']['strand'])
    eq_('+', out['baz']['strand'])
    eq_('+', out['foo']['strand'])

    ok_('read_IDs' not in out['bas'])
    ok_('read_count' not in out['bas'])
