from itertools import permutations

from mrjob.job import MRJob


class FilterInvalidPairs(MRJob):

    """
    TODO
    """

    def configure_options(self):
        """
        TODO
        """
        super(FilterCompletePair, self).configure_option()
        # TODO
        self.add_passthrough_option('--min-distance')
        self.add_passthrough_option('--max-distance')

    def mapper(self, key, alignment):
        yield alignment.base_id, alignment

    def reducer(self, base_id, alignments):
        alignments = list(alignments)

        for x, y in permutations(alignments, 2):

            if x != y and x.chromosome == y.chromosome and x.strand != y.strand:
                d = x.distance_to(y)

                if d > min_distance and d < max_distance:
                    if x.type == 'splat':
                        yield x.splat_id, x.read_id
                    if y.type == 'splat':
                        yield x.splat_id, y.read_id


if __name__ == '__main__':
    FilterInvalidPairs.run()
