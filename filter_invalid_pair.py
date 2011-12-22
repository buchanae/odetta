from itertools import combinations

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

from alignment import ID_base, distance_between


class FilterInvalidPair(MRJob):

    """
    TODO
    """

    INPUT_PROTOCOL = JSONProtocol

    def configure_options(self):
        """
        TODO
        """
        super(FilterInvalidPair, self).configure_options()
        self.add_passthrough_option('--min-distance', action='store',
                                    type=float, default=float('-inf'))
        self.add_passthrough_option('--max-distance', action='store',
                                    type=float, default=float('inf'))

    def mapper(self, ID, alignment):
        """
        TODO
        """
        yield ID_base(ID), (ID, alignment)

    def reducer(self, ID_base, alignments):
        """
        TODO
        """
        alignments = list(alignments)

        for (x_ID, x), (y_ID, y) in combinations(alignments, 2):

            if x != y and x['chromosome'] == y['chromosome'] and \
               x['strand'] != y['strand']:

                d = distance_between(x, y)
                if d >= self.options.min_distance and d <= self.options.max_distance:

                    if x['type'] == 'splat':
                        yield x, x_ID

                    if y['type'] == 'splat':
                        yield y, y_ID

    def duplicates_reducer(self, splat, IDs):
        """
        TODO
        """
        for ID in set(IDs):
            yield ID, splat

    def steps(self):
        """
        TODO
        """
        return [self.mr(mapper=self.mapper, reducer=self.reducer),
                self.mr(reducer=self.duplicates_reducer)]


if __name__ == '__main__':
    FilterInvalidPair.run()
