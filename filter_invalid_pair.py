from itertools import combinations

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

from alignment import ID_base, distance_between


class FilterInvalidPair(MRJob):

    """
    Filter paired alignments on a set of criteria including distance, strand, etc.

    --min-distance and --max-distance command-line options configure allowed distance.
    By default, any distance is allowed.
    """

    INPUT_PROTOCOL = JSONProtocol

    def configure_options(self):
        """Define command-line options."""

        super(FilterInvalidPair, self).configure_options()
        self.add_passthrough_option('--min-distance', action='store',
                                    type=float, default=float('-inf'))
        self.add_passthrough_option('--max-distance', action='store',
                                    type=float, default=float('inf'))

    def mapper(self, ID, alignment):
        """Group alignments by read ID base."""

        yield ID_base(ID), (ID, alignment)

    def reducer(self, ID_base, alignments):
        """
        Make alignment pairs and filter. Emit valid alignments individually.
        
        Only Splat alignments are returned, CashX alignments are not.

        Valid alignments must have...
          - the same chromosome
          - opposite strands
          - a distance between them within the given bounds.
        """

        valid = set()
        alignments = list(alignments)

        for ix, iy in combinations(xrange(len(alignments)), 2):
            x = alignments[ix][1]
            y = alignments[iy][1]

            if x['chromosome'] == y['chromosome'] and x['strand'] != y['strand']:

                d = distance_between(x, y)
                if d >= self.options.min_distance and d <= self.options.max_distance:

                    if x['type'] == 'splat':
                        valid.add(ix)

                    if y['type'] == 'splat':
                        valid.add(iy)

        for iv in valid:
            yield alignments[iv][0], alignments[iv][1]


if __name__ == '__main__':
    FilterInvalidPair.run()
