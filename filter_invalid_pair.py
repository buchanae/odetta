from itertools import permutations

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

from alignment import ID_base, distance_between


min_distance = 100
max_distance = 1000


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
        # TODO
        self.add_passthrough_option('--min-distance')
        self.add_passthrough_option('--max-distance')

    def mapper(self, ID, alignment):
        yield ID_base(ID), (ID, alignment)

    def reducer(self, ID_base, alignments):

        valid = set()
        alignments = list(alignments)
        for (x_ID, x), (y_ID, y) in permutations(alignments, 2):

            if x != y and x['chromosome'] == y['chromosome'] and \
               x['strand'] != y['strand']:


                d = distance_between(x, y)
                if d > min_distance and d < max_distance:

                    if x['type'] == 'splat':
                        yield x, x_ID

                    if y['type'] == 'splat':
                        yield y, y_ID

    def duplicates_reducer(self, splat, IDs):
        yield splat, IDs.next()

    def steps(self):
        return [self.mr(mapper=self.mapper, reducer=self.reducer),
                self.mr(reducer=self.duplicates_reducer)]


if __name__ == '__main__':
    FilterInvalidPair.run()
