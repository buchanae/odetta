from collections import Counter

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

from odetta.gff.feature import Feature
from odetta.gff.utils import transcript_splice_junctions


class ReferenceCountsBase(MRJob):

    """
    TODO
    """

    INPUT_PROTOCOL = JSONProtocol

    def configure_options(self):
        """Define command-line options."""

        super(ReferenceCountsBase, self).configure_options()
        # TODO check that file can be opened
        # TODO self.add_file_option('--rtree', help='TODO')

        self.add_file_option('--reference', help='TODO')


    def alignment_type(self, alignment):

        try:
            junctions = self.junctions[alignment['reference']]
        except KeyError:
            return 'complete'
        else:
            for j in junctions:
                if j >= alignment['start'] and j <= alignment['end']:
                    return 'edge'
            return 'complete'


    def mapper_init(self):
        """TODO"""
        features = Feature.from_file(self.options.reference)
        self.junctions = transcript_splice_junctions(features)


    def reducer(self, reference, values):
        """
        TODO
        """
        c = Counter()
        for v in values:
            c[v] += 1

        yield reference, c
