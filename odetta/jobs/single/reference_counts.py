from odetta.jobs.reference_counts_base import ReferenceCountsBase


class ReferenceCounts(ReferenceCountsBase):

    """
    TODO

    Look at ReferenceCountsBase, it defines most of the code shared by single/paired
    reference count jobs.
    """

    def mapper(self, key, alignment):
        """
        TODO
        """
        yield alignment['reference'], self.alignment_type(alignment)


if __name__ == '__main__':
    ReferenceCounts.run()
