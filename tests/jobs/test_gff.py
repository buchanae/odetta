from collections import defaultdict

import gff
from mrjob.protocol import PickleProtocol
from nose.tools import eq_, ok_

from jobs.gff.base import GFFJob
from jobs.gff import *
from tests import filepath, disable_mrjob_loggers


#disable_mrjob_loggers()


def test_parse_line():
    j = GFFJob()
    f = j.parse_line('Chr1\tTAIR10\tgene\t2\t20\t.\t+\t.\tID=Gene1')
    eq_(gff.Feature, type(f))

    
def test_Filter():
    f = filepath('a.gff')
    j = Filter().sandbox(f)
    j.run_mapper()
    out = j.parse_output(PickleProtocol)

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

