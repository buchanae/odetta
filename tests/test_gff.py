from nose.tools import eq_

from odetta.gff.feature import Feature
from odetta.gff.utils import transcript_splice_junctions

from tests import dummy


def test_transcript_splice_junctions():
    f = dummy('g.gff')
    features = Feature.from_file(f.name)
    juncs = transcript_splice_junctions(features)
    eq_({
        'Chr1_40.1': [220, 302],
        'Chr1_364.1': [83],
        'Chr1_366.1': [90, 196, 326, 535],
    }, juncs)
