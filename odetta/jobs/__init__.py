import gff
import pairs
import parse

#TODO generate this automatically
names = {
    'gff.filter': gff.Filter,
    'gff.overlap': gff.Overlap,
    'gff.transcriptome': gff.Transcriptome,
    'pairs.combiner': pairs.Combiner,
    'pairs.distance-statistics': pairs.DistanceStatistics,
    'pairs.incomplete-filter': pairs.IncompleteFilter,
    'pairs.reference-counts': pairs.ReferenceCounts,
    'pairs.to-splat': pairs.ToSplat,
    'pairs.unambiguous-filter': pairs.UnambiguousFilter,
    'pairs.valid-filter': pairs.ValidFilter,
    'parse.bowtie': parse.Bowtie,
    'parse.sam': parse.SAM,
    'parse.splat': parse.Splat,
    'parse.split-splat': parse.SplitSplat,
}
