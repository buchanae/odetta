import gff


class Feature(gff.Feature):

    """TODO"""

    @property
    def ID(self):
        try:
            return self.attributes['ID']
        except KeyError:
            return ''

    @property
    def parents(self):
        try:
            return self.attributes.as_list('Parent')
        except KeyError:
            return []
