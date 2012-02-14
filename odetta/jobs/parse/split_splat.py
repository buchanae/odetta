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
            if len(ID) > 0 and ID[0] in ('+', '-'):
                splat['ID'] = ID[1:]
                splat['strand'] = ID[0]
            else:
                splat['ID'] = ID
                splat['strand'] = '+'

            yield key, splat


if __name__ == '__main__':
    SplitSplat.run()
