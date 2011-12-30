from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, RawValueProtocol


class CombineSplats(MRJob):

    """
    Combine Splat alignments.  The opposite of SplitSplat.

    Reads JSON data and emits Splat strings.
    """

    INPUT_PROTOCOL = JSONProtocol
    OUTPUT_PROTOCOL = RawValueProtocol

    def mapper(self, ID, splat):
        """Group data by read ID."""

        yield splat, ID

    def reducer(self, splat, IDs):
        """Combine and emit Splat strings."""

        IDs = list(IDs)
        yield None, splat['template'].format(read_count=len(IDs), IDs=','.join(IDs))


if __name__ == '__main__':
    CombineSplats.run()
