from collections import Counter

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol


class ReferenceCounts(MRJob):

    """
    TODO
    """

    INPUT_PROTOCOL = JSONProtocol

    def mapper(self, key, pair):
        """
        TODO
        """
        yield pair[0]['reference'], pair

    def reducer(self, reference, pairs):
        """
        TODO
        """
        c = Counter()

        for x, y in pairs:
            k = '-'.join(sorted([x['type'], y['type']]))
            c[k] += 1

        yield reference, c


if __name__ == '__main__':
    ReferenceCounts.run()
