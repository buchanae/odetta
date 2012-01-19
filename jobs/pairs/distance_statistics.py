import math

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

from utils import distance_between


class DistanceStatistics(MRJob):

    """
    Calculate statistics on the distance between paired alignments.

    Calculates the mean and standard deviation.
    """

    INPUT_PROTOCOL = JSONProtocol
    # necessary for aggregating one set of statistics.
    JOBCONF = {'mapreduce.job.maps': '1'}

    def mapper_init(self):
        self.mean = 0.0
        self.ssr = 0.0
        self.n = 0.0

    def mapper(self, key, pair):
        """Calculate running statistics for each alignment pair."""

        x, y = pair
        d = distance_between(x, y)
        self.n += 1
        tmp = self.mean + ((d - self.mean) / self.n)
        self.ssr += (d - self.mean) * (d - tmp)
        self.mean = tmp

    def mapper_final(self):
        """Emit statistics."""
        
        var = self.ssr / self.n
        std = math.sqrt(var)
        yield None, (self.mean, std)


if __name__ == '__main__':
    DistanceStatistics.run()
