from tempfile import NamedTemporaryFile

from nose.tools import eq_, ok_

from odetta.jobs.gff.transcriptome import Transcriptome
from tests import *


disable_mrjob_loggers()


def read_fasta(f):
    d = {}
    while True:
        try:
            line = f.next().strip()
            if line != '' and line[0] == '>':
                d[line] = f.next().strip()
        except StopIteration:
            break

    return d


def test_Transcriptome_load_genome():
    g = dummy('genome.fas')
    j = Transcriptome(args=['--genome', g.name])
    j.reducer_init()

    eq_(2, len(j.genome))
    ok_('Chr1' in j.genome)
    ok_('Chr2' in j.genome)
    eq_('ATCGTGCTAGTCTGATGCATTGGTATG', str(j.genome['Chr1']))


def test_Transcriptome():
    e = read_fasta(dummy('expected'))
    f = dummy('d.gff')
    g = dummy('genome.fas')
    o = NamedTemporaryFile()
    j = Transcriptome(args=['--genome', g.name]).sandbox(f, o)
    j.run_job()

    # not a pretty way to test this, but the order of the output 
    # can't be expected in any order, and the records are multi-line,
    # so sorting isn't trivial.  it works.
    o = read_fasta(open(o.name))
    eq_(e, o)
