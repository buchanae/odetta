from mrjob.job import MRJob


class CombineSplats(MRJob):
    def reducer(self, splat_row, splats):
        yield reduce(lambda x, y: x.merge(y), splats)


if __name__ == '__main__':
    CombineSplats.run()
