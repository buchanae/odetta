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


def model_parser(fields):

    """
    Help create a dictionary from tokens, with default fields and types.

    Fields are defined in order, to match tokens parsed from a line (e.g. TSV).

    For example,
        m = model([
            ('foo', 'bar'),
            ('baz', 0),
            ('bat', 'fuuu'),
        ])

        a = model('one\t1'.split('\t'))

        a['foo'] == 'one'
        a['baz'] == 1      # notice the type conversion from string to int
        a['bat'] == 'fuuu' # notice the default value from the field definition

    Not a general parser! but useful nonetheless.
    """

    def make(tokens):
        data = {}
        for i, field in enumerate(fields):
            k = field[0]
            if i < len(tokens):
                # convert token to type defined by field default
                v = type(field[1])(tokens[i])
            else:
                v = field[1]
            data[k] = v

        return data

    return make
