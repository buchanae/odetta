def ID_base(ID):
    return ID.split('\\')[0]


def distance_between(a, b):
    """Return the distance between to two alignments."""

    if a['start'] < b['start']:
        return b['start'] - a['end']
    else:
        return a['start'] - b['end']


def parse_SAM(raw):
    data = {}
    fields = raw.split('\t')

    flag = int(fields[1])
    sequence = fields[9]

    data['ID'] = fields[0]
    data['chromosome'] = fields[2]
    data['start'] = int(fields[3])
    data['end'] = data['start'] + len(sequence)

    # The SAM format stores strand info in a bitwise flag,
    # not obscure at all...
    data['strand'] = '-1' if flag & 16 else '1'
    data['type'] = 'SAM'

    return data


def parse_splat(raw):
    data = {}
    fields = raw.split('\t')

    data['template'] = '\t'.join(fields[:10] + ['{read_count}', '{IDs}'] + fields[12:])
    data['chromosome'] = fields[0]

    try:
        data['IDs'] = [x for x in fields[11].split(',')]
    except IndexError:
        data['IDs'] = []

    try:
        data['strand'] = fields[12]
    except IndexError:
        data['strand'] = None

    a = int(fields[5])
    b = int(fields[7])
    data['start'] = a if a < b else b

    a = int(fields[6])
    b = int(fields[8])
    data['end'] = a if a > b else b
    data['type'] = 'splat'

    return data
