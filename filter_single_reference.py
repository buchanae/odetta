from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol


class FilterPairSingleReference(MRJob):

    """
    """

    INPUT_PROTOCOL = JSONProtocol

    #TODO invert option

    def mapper(self, key, pair):
        """
        """
        yield (pair[0]['ID'], pair[1]['ID']), pair

    def reducer(self, key, pairs):
        refs = set()
        pairs = list(pairs)

        for pair in pairs:
            refs.add(pair[0]['reference'])
            refs.add(pair[1]['reference'])

        if len(refs) > 1:
            for p in pairs:
                yield p


if __name__ == '__main__':
    FilterPairSingleReference.run()
