def ID_base(ID):
    """
    Return the base of a read ID.

    For example, given read ID "Foo\1" the base is "Foo".
    """
    return ID.split('\\')[0]


def distance_between(a, b):
    """
    Return the distance between to two alignments.

    Overlaps are returned as negative distance.
    """
    a, b = sorted([a, b], key=lambda x: x['start'])
    return b['start'] - a['end']
