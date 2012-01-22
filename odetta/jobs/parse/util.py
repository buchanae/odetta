def model(fields):

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
