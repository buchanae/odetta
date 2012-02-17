import os


#TODO there is a better way to define all this
_base = os.path.dirname(os.path.abspath(__file__))
_path = lambda *x: os.path.join(_base, *x)
_gff = lambda x: _path('gff', x)
_pairs = lambda x: _path('pairs', x)
_parse = lambda x: _path('parse', x)
_single = lambda x: _path('single', x)

job_path = {
    'gff.blast': _gff('blast.py'),
    'gff.filter': _gff('filter.py'),
    'gff.overlap': _gff('overlap.py'),
    'gff.transcriptome': _gff('transcriptome.py'),
    'pairs.combiner': _pairs('combiner.py'),
    'pairs.distance_filter': _pairs('distance_filter.py'),
    'pairs.distance_statistics': _pairs('distance_statistics.py'),
    'pairs.reference_counts': _pairs('reference_counts.py'),
    'pairs.to_splat': _pairs('to_splat.py'),
    'pairs.unambiguous_filter': _pairs('unambiguous_filter.py'),
    'parse.bowtie': _parse('bowtie.py'),
    'parse.sam': _parse('sam.py'),
    'parse.splat': _parse('splat.py'),
    'parse.split_splat': _parse('split_splat.py'),
    'single.reference_counts': _single('reference_counts.py'),
}
