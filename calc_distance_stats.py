from mrjob.job import MRJob


def pair_distance_stats(pairs):
    """
    Calculate the average and standard deviation of distance between paired alignments.
    """
    # TODO unit test for this
    # TODO test and code for handling len(pairs) == 1 or len(pairs) == 0
    mean = 0.0
    ss = 0.0
    n = 0

    for a, b in pairs:
        d = float(a.distance_to(b))
        n += 1
        prev = mean
        mean = prev + ((d - prev) / float(n))
        ss = ss + (d - prev) * (d - mean)

    var = ss / (n - 1)
    std = math.sqrt(var)

    return var, std

class CalcDistanceStats(MRJob):

    """
    TODO
    """

    def configure_options(self):
        pass

    def mapper(self, key, line):
        """
        TODO
        """
        pass

    def reducer(self, ID_base, alignments):
        """
        TODO
        """
        pass


if __name__ == '__main__':
    CalcDistanceStats.run()
