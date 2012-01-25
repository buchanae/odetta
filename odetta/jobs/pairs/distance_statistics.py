
from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, PickleProtocol, ReprProtocol

from stats import Stats

from odetta.utils import distance_between


class DistanceStatistics(MRJob):

    """
    Calculate statistics on the distance between paired alignments.

    Calculates the mean and standard deviation.
    """

    INPUT_PROTOCOL = JSONProtocol
    INTERNAL_PROTOCOL = PickleProtocol
    OUTPUT_PROTOCOL = ReprProtocol

    # necessary for aggregating one set of statistics.
    JOBCONF = {'mapreduce.job.reduces': '1'}

    def mapper_init(self):
        self.stats = {
            'gap': Stats(),
            'overlap': Stats(),
        }


    def mapper(self, key, pair):
        """Calculate running statistics for each alignment pair."""

        x, y = pair
        d = distance_between(x, y)

        if d < 0:
            self.stats['overlap'].add_data(d * -1)
        else:
            self.stats['gap'].add_data(d)


    def mapper_final(self):
        """Emit statistics."""

        yield 'Gaps', self.stats['gap']
        yield 'Overlaps', self.stats['overlap']

    def reducer(self, key, stats):
        yield key, str(reduce(lambda x, y: x + y, stats))


if __name__ == '__main__':
    DistanceStatistics.run()
