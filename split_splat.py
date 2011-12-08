from mrjob.job import MRJob

from alignment import Alignment


class SplitSplat(MRJob):

    """
    TODO
    """

    def mapper(self, key, line):
        for splat in Splat.from_string(line).split():
            yield splat

if __name__ == '__main__':
    SplitSplat.run()
