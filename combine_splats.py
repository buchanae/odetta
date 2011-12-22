from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, RawValueProtocol


class CombineSplats(MRJob):

    INPUT_PROTOCOL = JSONProtocol
    OUTPUT_PROTOCOL = RawValueProtocol

    def mapper(self, ID, splat):
        yield splat, ID

    def reducer(self, splat, IDs):
        IDs = list(IDs)
        yield None, splat['template'].format(read_count=len(IDs), IDs=','.join(IDs))


if __name__ == '__main__':
    CombineSplats.run()
