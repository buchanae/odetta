from collections import defaultdict

from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol


class CountReferenceHits(MRJob):

    """
    """

    INPUT_PROTOCOL = JSONProtocol

    # TODO optionally pass in gff file?

    def mapper(self, key, pair):
        """
        """
        yield pair[0]['reference'], pair

    def reducer(self, reference, pairs):
        d = defaultdict(lambda: 0)

        for x, y in pairs:
            d['total'] += 1
            k = x['type'] + '-' + y['type']
            d[k] += 1

        yield reference, d


if __name__ == '__main__':
    CountReferenceHits.run()
