from nose.tools import eq_, ok_

from jobs.parse import *
from jobs.parse.util import model
from tests import filepath, disable_mrjob_loggers


disable_mrjob_loggers()


def test_model():
    m = model([
      ('one', ''),
      ('two', 0),
      ('three', 'd'),
    ])

    b = m(['foo', '1'])
    eq_('foo', b['one'])
    eq_(1, b['two'])
    eq_('d', b['three'])


def test_SAM():
    f = filepath('sam')
    j = SAM().sandbox(f)
    j.run_job()
    out = dict((x[1]['ID'], x) for x in j.parse_output())

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


def test_SAM_type():
    f = filepath('sam')
    j = SAM(args=['--type', 'blah']).sandbox(f)
    j.run_job()
    out = j.parse_output()

    k, v = out[0]
    eq_('blah', v['type'])


def test_Splat():
    f = filepath('splat')
    j = Splat().sandbox(f)
    j.run_job()
    out = j.parse_output()
    out = dict((x[1]['reference'], x) for x in j.parse_output())

    eq_(3, len(out))

    k, v = out['ChrC']
    eq_(None, k)
    eq_('ChrC', v['reference'])
    eq_(1, v['start'])
    eq_(4, v['end'])
    eq_('bas,baz', v['read_IDs'])
    eq_('-', v['strand'])

    k, v = out['ChrB']
    eq_('+', v['strand'])

    k, v = out['ChrA']
    eq_('', v['read_IDs'])
    eq_('+', v['strand'])

def test_SplitSplat():
    f = filepath('splat')
    j = SplitSplat().sandbox(f)
    j.run_job()
    out = j.parse_output()

    eq_(['', 'bas', 'baz', 'foo'], sorted([x[1]['ID'] for x in out]))
    ok_('read_IDs' not in x[1])
    ok_('read_count' not in x[1])
