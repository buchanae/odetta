from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol


class SplitSplat(MRJob):

    INPUT_PROTOCOL = JSONProtocol

    def mapper(self, key, splat):

        IDs = splat['read_IDs'].split(',')

        del splat['read_count']
        del splat['read_IDs']

        for ID in IDs:
            splat['ID'] = ID
            yield key, splat



if __name__ == '__main__':
    SplitSplat.run()
