import gff
from nose.tools import eq_, ok_

from jobs.gff.base import GFFJob


disable_mrjob_loggers()


def test_parse_line():
    j = GFFJob()
    f = j.parse_line('Chr1\tTAIR10\tgene\t2\t20\t.\t+\t.\tID=Gene1')
    eq_(gff.Feature, type(f))
