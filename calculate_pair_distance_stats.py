import math

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

from utils import distance_between


class CalculatePairDistanceStats(MRJob):

    """
    Calculate statistics on the distance between paired alignments.

    Calculates the mean and standard deviation.
    """

    INPUT_PROTOCOL = JSONProtocol

    # necessary for returning one set of statistics.
    # TODO there is probably a way to get around this.
    JOBCONF = {'mapreduce.job.reduces': '1'}

    def reducer_init(self):
        self.mean = 0.0
        self.ssr = 0.0
        self.n = 0.0

    def reducer(self, key, pair):
        """Calculate running statistics for each alignment pair."""

        d = distance_between(x, y)
        self.n += 1
        tmp = self.mean + ((d - self.mean) / self.n)
        self.ssr += (d - self.mean) * (d - tmp)
        self.mean = tmp

    def reducer_final(self):
        """Emit statistics."""
        
        var = self.ssr / self.n
        std = math.sqrt(var)
        yield None, (self.mean, std)


if __name__ == '__main__':
    CalculatePairDistanceStats.run()
