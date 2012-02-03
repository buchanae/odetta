from collections import defaultdict

from nose.tools import eq_, ok_

from odetta.jobs.gff.filter import calc_coverage, Filter
from tests import *


disable_mrjob_loggers()

mRNAs = [
    'Chr1\tTAIR10\tmRNA\t12\t25\t.\t+\t.\tID=mRNA1.2\n',
    'Chr1\tTAIR10\tmRNA\t2\t10\t.\t+\t.\tID=mRNA1.1\n',
    'Chr2\tTAIR10\tmRNA\t65\t90\t.\t+\t.\tID=mRNA3.1\n',
]


def test_Filter_mapper():
    f = dummy('a.gff')
    j = Filter().sandbox(f)
    j.run_mapper()
    out = j.parse_output(Filter.INTERNAL_PROTOCOL)

    eq_(8, len(out))

    d = defaultdict(list)
    for ID, f in out:
        d[ID].append(f)

    e = sorted([f.attributes['ID'] for f in d['mRNA1.1']])
    eq_(['exon1', 'exon2', 'mRNA1.1'], e)

    e = sorted([f.attributes['ID'] for f in d['mRNA1.2']])
    eq_(['exonA', 'exonB', 'mRNA1.2'], e)

    e = sorted([f.attributes['ID'] for f in d['mRNA3.1']])
    eq_(['exonX', 'mRNA3.1'], e)


def test_Filter_load_counts():
    f = dummy('counts')
    j = Filter(args=['--counts', f.name])
    j.reducer_init()

    eq_(15, j.total)
    eq_(2, len(j.counts))
    eq_({'a': 3, 'b': 2}, j.counts['foo'])
    eq_({'a': 5, 'b': 5}, j.counts['bar'])


def test_calc_coverage():
    eq_(0.03130878130878131, calc_coverage(253, 650000000, 12432))
    eq_(0, calc_coverage(0, 650000000, 12432))


@dummytest(Filter(), 'a.gff')
def test_Filter(out):
    out = sorted([x[1] for x in out])
    eq_(mRNAs, out)


@dummytest(Filter(), 'e.gff')
def test_Filter_no_parent_mrna(out):
    out = sorted([x[1] for x in out])
    eq_(mRNAs[:2], out)


@dummytest(Filter(args=['--max-length', '13']), 'a.gff')
def test_Filter_max_length(out):
    out = sorted([x[1] for x in out])
    eq_([mRNAs[1]], out)


@dummytest(Filter(args=['--min-length', '13']), 'a.gff')
def test_Filter_min_length(out):
    out = sorted([x[1] for x in out])
    eq_([mRNAs[0], mRNAs[2]], out)


@dummytest(Filter(args=['--min-length', '13', '--max-length', '14']), 'a.gff')
def test_Filter_length(out):
    out = sorted([x[1] for x in out])
    eq_([mRNAs[0]], out)


@dummytest(Filter(args=['--min-exons', '4']), 'c.gff')
def test_Filter_min_exons(out):
    out = sorted([x[1] for x in out])
    eq_(mRNAs[:2], out)


@dummytest(Filter(args=['--max-exons', '4']), 'c.gff')
def test_Filter_max_exons(out):
    out = sorted([x[1] for x in out])
    eq_(mRNAs[1:], out)


@dummytest(Filter(args=['--min-exons', '5', '--max-exons', '7']), 'c.gff')
def test_Filter_exons(out):
    out = sorted([x[1] for x in out])
    eq_([mRNAs[0]], out)


@dummytest(Filter(args=['--counts', dummy('b.counts').name, '--min-coverage', '25000', 
                        '--max-coverage', '100000']), 'b.gff')
def test_Filter_coverage(out):
    out = sorted([x[1] for x in out])
    eq_(['Chr2\tTAIR10\tmRNA\t15000\t18000\t.\t+\t.\tID=mRNA3.1\n'], out)
