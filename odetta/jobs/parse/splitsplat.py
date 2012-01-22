from splat import Splat


class SplitSplat(Splat):

    """
    Parse a Splat formatted line, splitting each in multiple records,
    one for each read ID.
    """

    def mapper(self, key, value):

        splat = self.parse_line(value)

        IDs = splat['read_IDs'].split(',')

        del splat['read_count']
        del splat['read_IDs']

        for ID in IDs:
            splat['ID'] = ID
            yield key, splat


if __name__ == '__main__':
    SplitSplat.run()
