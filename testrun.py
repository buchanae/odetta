"""
TODO
"""

from glob import glob
import os
import shlex
import subprocess

#TODO need logging, timing, and CPU/mem usage
#TODO test case for this script

#TODO link all these to the working dir
#create mrjob.conf

BOWTIE_EXE = 'bowtie'
BOWTIE_BUILD_EXE = 'bowtie-build'
GMB_EXE = ''
MULTISPLAT_EXE = ''
REFERENCE_GFF = '/path/to/TAIR.gff'
REFERENCE_FASTA = ''
REFERENCE_DIR = os.path.dirname(REFERENCE_FASTA)
READS_PATHS = glob('/reads_dir/*.fasta')
SPLIT_SIZE = '25000000'


class cmd(str):
    def run(self, *args):
        sp = shlex.split(self.format(*args))
        subprocess.Popen(sp)
        

bowtie_build = cmd('bin/bowtie-build --offrate 1 {} {}')

bowtie = cmd('bin/bowtie -f -p 8 -v 0 -S --sam-nohead -a {} {} {}')

bowtie_unaligned = cmd(bowtie + ' --un {}')

split = cmd('split --lines={} {} {}')

splat = cmd('bin/multisplat splat -t 8 -f {} -r {} -n 1000 -x 5000 -c 40 -i 41 -S 1')

stack = cmd('bin/multisplat stack -s {} -r {} -n 1 -c 2 -o {}')

gmb = cmd('bin/gmb -r {} -a {} -s {} -o {}')

job = cmd('python jobs/{}.py --conf-path conf/mrjob.conf {} > {}')


if __name__ == '__main__':

    ref_base = os.path.basename('reference.fasta')
    if not os.path.exists('reference.1.ebwt'):
        bowtie_build.run('reference.fasta', 'reference')

    bowtie_unaligned.run('reference', ','.join(READS_PATHS), 
                         'aligned.sam', 'unaligned.fasta')

    job.run('parse/sam', 'aligned.sam', 'aligned.json')

    job.run('pairs/incomplete_filter', 'aligned.json', 'incomplete_aligned.json')

    split.run(SPLIT_SIZE, 'unaligned.fasta', 'split-unaligned')

    for i, p in enumerate(glob('split-unaligned*')):
        splat.run(p, 'reference.fasta')

    job.run('parse/splitsplat', 
            ' '.join(glob('split-unaligned*.supersplat')), 'splat.json')

    job.run('pairs/combiner', 'splat.json incomplete_aligned.json', 'pairs1.json')

    job.run('pairs/distance_statistics', 'pairs1.json', 'dist_pairs1.json')

    #TODO min_d, max_d
    #dist_opt = '--min-distance {} --max-distance {}'.format(min_d, max_d)
    dist_opt = ''
    job.run('pairs/valid_filter', '{} pairs1.json'.format(dist_opt), 'valid1.json')

    job.run('pairs/to_splat', 'valid1.json', 'valid.splat')

    stack.run('valid.splat', 'reference.fasta', 'stack.out')

    gmb.run('reference.fasta', 'combined_alignments.sam', 'stack.out', 'gmb.gff')

    job.run('gff/transcriptome', '--genome reference.fasta gmb.gff',
            'gmb_transcriptome.fasta')

    if not os.path.exists('gmb_transcriptome.1.ebwt'):
        bowtie_build.run('gmb_transcriptome.fasta', 'gmb_transcriptome')

    bowtie.run('gmb_transcriptome', ','.join(READS_PATHS), 'gmb-aligned.sam')

    job.run('parse/sam', 'gmb-aligned.sam', 'gmb_alignments.json')

    job.run('pairs/combiner', 'gmb_alignments.json', 'gmb_pairs.json')

    job.run('pairs/distance_statistics', 'gmb_pairs.json', 'dist_gmb_pairs.json')

    #TODO min_d, max_d
    #dist_opt = '--min-distance {} --max-distance {}'.format(min_d, max_d)
    dist_opt = ''
    #TODO coverage estimate and filter
    job.run('pairs/valid_filter', '{} gmb_pairs.json'.format(dist_opt), 'gmb_valid.json')

    job.run('pairs/unambiguous_filter', 'gmb_valid.json', 'gmb_valid_unambig.json')

    job.run('pairs/reference_counts', 'gmb_valid_unambig.json', 'gmb_pair_counts.json')

    job.run('gff/filter', 
        '--counts gmb_pair_counts.json --min-length 300 --min-exons 2 gmb.gff',
        'gmb_filtered_mRNAs.gff')

    job.run('gff/overlap', 
        '--reference reference.gff --min-overlap 0.8 gmb_filtered_mRNAs.gff',
        'overlapped.gff')
