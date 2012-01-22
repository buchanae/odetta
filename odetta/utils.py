def ID_base(ID):
    """
    Return the base of a read ID.

    For example, given read ID "Foo\1" the base is "Foo".
    """
    return ID.split('\\')[0]


def distance_between(a, b):
    """Return the distance between to two alignments."""

    if a['start'] < b['start']:
        return b['start'] - a['end']
    else:
        return a['start'] - b['end']
