from mrjob.job import MRJob

from alignment import parse_splat


class SplitSplat(MRJob):

    """
    TODO
    """

    def mapper(self, key, line):
        splat = parse_splat(line)

        for ID in splat['IDs']:
            yield ID, splat

if __name__ == '__main__':
    SplitSplat.run()
