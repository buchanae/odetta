import math

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, ReprProtocol

from odetta.utils import distance_between


class Stats(object):
    def __init__(self):
        self.mean = 0.0
        self.ssr = 0.0
        self.n = 0.0

    def add(self, val):
        self.n += 1
        tmp = self.mean + ((val - self.mean) / self.n)
        self.ssr += (val - self.mean) * (val - tmp)
        self.mean = tmp

    @property
    def variance(self):
        if self.n > 0:
            return self.ssr / self.n
        else:
            return 0.0

    @property
    def standard_deviation(self):
        return math.sqrt(self.variance)

    def __str__(self):
        s = 'Mean: {}, Standard Deviation: {}, Variance: {}, N: {}'
        return s.format(self.mean, self.standard_deviation, self.variance, self.n)


class DistanceStatistics(MRJob):

    """
    Calculate statistics on the distance between paired alignments.

    Calculates the mean and standard deviation.
    """

    INPUT_PROTOCOL = JSONProtocol
    OUTPUT_PROTOCOL = ReprProtocol

    # necessary for aggregating one set of statistics.
    JOBCONF = {'mapreduce.job.maps': '1'}

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
            self.stats['overlap'].add(d * -1)
        else:
            self.stats['gap'].add(d)


    def mapper_final(self):
        """Emit statistics."""

        yield 'Gaps', str(self.stats['gap'])
        yield 'Overlaps', str(self.stats['overlap'])


if __name__ == '__main__':
    DistanceStatistics.run()
