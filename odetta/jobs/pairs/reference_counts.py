from collections import Counter, defaultdict
from itertools import ifilter

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

from odetta.gff.feature import Feature
from odetta.gff.utils import transcript_splice_junctions


class ReferenceCounts(MRJob):

    """
    TODO
    """

    INPUT_PROTOCOL = JSONProtocol

    def configure_options(self):
        """Define command-line options."""

        super(ReferenceCounts, self).configure_options()
        # TODO check that file can be opened
        # TODO self.add_file_option('--rtree', help='TODO')

        self.add_file_option('--reference', help='TODO')


    def mapper_init(self):
        """TODO"""
        features = Feature.from_file(self.options.reference)
        self.junctions = transcript_splice_junctions(features)


    def mapper(self, key, pair):
        """
        TODO
        """
        x, y = pair

        ref = x['reference']

        def overlaps(start, end, junctions):
            for e in junctions:
                if e >= start and e <= end:
                    return True
            return False

        try:
            junctions = self.junctions[ref]
        except KeyError:
            x_type = y_type = 'complete'
        else:
            x_type = 'edge' if overlaps(x['start'], x['end'], junctions) else 'complete'
            y_type = 'edge' if overlaps(y['start'], y['end'], junctions) else 'complete'

        yield ref, '-'.join(sorted([x_type, y_type]))


    def reducer(self, reference, values):
        """
        TODO
        """
        c = Counter()
        for v in values:
            c[v] += 1

        yield reference, c


if __name__ == '__main__':
    ReferenceCounts.run()
