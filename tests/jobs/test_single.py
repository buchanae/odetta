from nose.tools import eq_, ok_

from odetta.jobs.single.reference_counts import ReferenceCounts
from tests import *


disable_mrjob_loggers()


@dummytest(ReferenceCounts(args=['--reference', 'tests/dummies/g.gff']), 
           'reference_counts_alignments_single')
def test_reference_counts(out):
    eq_({
      'Chr1_40.1': {
          'complete': 1,
          'edge': 2,
      },
    }, dict((x[0], x[1]) for x in out))
