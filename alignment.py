class Alignment(object):

    """Base class for alignment data."""

    def __init__(self):
        pass

    @property
    def base_id(self):
        """
        Return the base of a read ID.

        For example, the base ID of FooBar\1 is FooBar.
        """
        return self.id.split('\\')[0]

    @property
    def is_paired(self):
        return self.id[-2:] == '\\1' or self.id[-2:] =='\\2'

    @property
    def pair_id(self):
        """
        TODO
        """
        return self.id[:-1]
        
    @property
    def sister_id(self):
        """
        Return the sister ID of a paired read ID.

        For example, the sister of FooBar\1 is FooBar\2.
        """
        return self.base_id + '\\2' if self.pair_id == '1' else '\\2'

    def distance_to(self, other):
        """Return the distance between to this alignment and another."""
        if self.start < other.start:
            return other.start - self.end
        else:
            return self.start - other.end


class SAM(Alignment):

    """TODO"""

    @property
    def strand(self):
        """TODO"""
        pass


class Splat(Alignment):

    """TODO"""

    fields = ('chromosome', 'flanks', 'a_length', 'b_length', 'intron_length', 
              'a_begin', 'a_end', 'b_begin', 'b_end', 'sequence')

    def merge(self, *others):
        """TODO"""
        #TODO check that fields are the same
        # TODO don't duplicate read IDs
        pass
