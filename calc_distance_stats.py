from itertools import combinations
import math

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol

from alignment import ID_base, distance_between


class CalcDistanceStats(MRJob):

    """
    TODO
    """

    INPUT_PROTOCOL = JSONProtocol
    JOBCONF = {'mapreduce.job.reduces': '1'}

    def mapper(self, ID, alignment):
        """
        TODO
        """
        yield ID_base(ID), alignment

    def reducer_init(self):
        self.mean = 0.0
        self.ssr = 0.0
        self.n = 0.0

    def reducer(self, ID_base, alignments):
        """
        TODO
        """
        alignments = list(alignments)

        for x, y in combinations(alignments, 2):
            d = distance_between(x, y)
            self.n += 1
            tmp = self.mean + ((d - self.mean) / self.n)
            self.ssr += (d - self.mean) * (d - tmp)
            self.mean = tmp

    def reducer_final(self):
        var = self.ssr / self.n
        std = math.sqrt(var)
        yield None, (self.mean, std)


if __name__ == '__main__':
    CalcDistanceStats.run()
