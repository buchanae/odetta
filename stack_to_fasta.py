import argparse


def stack_to_fasta(path):
    counter = 0
    with open(path) as fh:
        for line in fh:
            if line[0] != '@':
                sp = line.strip().split('\t')
                count = int(sp[0])
                for i in xrange(count):
                    yield '>Stack_{0}'.format(counter)
                    yield sp[1]
                    counter += 1


if __name__ == '__main__':
    parser.add_argument('stack', help='TODO')
    args = parser.parse_args()
    for line in stack_to_fasta(args.stack):
        print line
