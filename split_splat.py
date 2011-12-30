from mrjob.job import MRJob

from alignment import parse_splat


class SplitSplat(MRJob):

    """
    Split Splat records into multiple records with one read per record.

    Splat records contain multiple read IDs i.e. one-to-many.
    We need to work with read IDs individually i.e. one-to-one.
    This converts one-to-many -> one-to-one.

    For example, given...

      SplatDataA, Read1,Read2,Read3

    ...this will emit...
      Read1 SplatDataA
      Read2 SplatDataA
      Read3 SplatDataA
    """

    def mapper(self, key, line):
        splat = parse_splat(line)

        for ID in splat['IDs']:
            yield ID, splat

if __name__ == '__main__':
    SplitSplat.run()
