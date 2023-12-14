import os
import subprocess

bwavg = '/projects/ps-renlab2/earmand/conda_envs/bigwigtools/bin/bigWigAverageOverBed'
bedtools  = '/projects/ps-renlab2/earmand/conda_envs/bedtools/bin/bedtools'



map_score = '../hg38/k{}_map_score.bw'
bismap_score = '../hg38/bismap_k50_score.bw'

peak_regions = '../hg38/human_peaks_{}bp.bed'
peak_sizes = [
    500,
    2000,
    4000
]
k_len = [50, 100, 24, 36, ]

hg38_lengths = '../hg38/human_chrom_size'

outfile_peaks = '../outs/human_non_peak_background_{}bp.bed'
outfile_score = '../outs/human_non_peak_regions_mappability_scores_k{}_{}bp.txt'
outfile_bed_score = '../outs/human_non_peak_regions_mappability_scores_k{}_{}bp.bed'
outfile_counts = '../outs/human_non_peak_regions_counts_{}bp.bed'
bamfile = '/oasis/tscc/scratch/earmand/scratch/human_atac_unbiased_nodup_bam_merge_sort.bam'

outfile_counts_peaks = '../outs/human_peak_regions_counts_{}bp.bed'

outfile_score_peaks = '../outs/human_peak_regions_mappability_k{}_scores_{}bp.txt'
outfile_bed_score_peaks = '../outs/human_peak_regions_mappability__k{}_scores_{}bp.bed'

for size in peak_sizes:
    regions = peak_regions.format(size)
    out_peaks = outfile_peaks.format(size)
    out_counts = outfile_counts.format(size)
    
    out_counts_peaks = outfile_counts_peaks.format(size)

    #############################################################
    #        get paired non-peak regions
    #############################################################
    # shuffle_str = f'{bedtools} shuffle -i {regions} -g {hg38_lengths} -excl {regions} -f .25 -chrom -seed 23 > {out_peaks} '
    # os.system(shuffle_str)
 
    #############################################################
    #        Calucluate mappability score
    #############################################################
    for k in k_len:
        out_scores = outfile_score.format(k, size)
        out_bed_scores = outfile_bed_score.format(k, size)
        out_scores_peaks = outfile_score_peaks.format(k, size)
        out_bed_scores_peaks = outfile_bed_score_peaks.format(k, size)
        map_score_k = map_score.format(k)
    

        bw_avg_bg_str = f'{bwavg} {map_score_k} {out_peaks} {out_scores} -bedOut={out_bed_scores} '
        bw_avg_peak_str = f'{bwavg} {map_score_k} {regions} {out_scores_peaks} -bedOut={out_bed_scores_peaks} '
        os.system(bw_avg_bg_str)
        # os.system(bw_avg_peak_str)

    # count_reads_str = f'{bedtools}  multicov -bams {bamfile} -bed {out_peaks} -q 30 > {out_counts}'
    # count_reads_peaks_str = f' {bedtools}  multicov -bams {bamfile} -bed {regions} -q 30 > {out_counts_peaks} '
    # os.system(count_reads_str)
    # os.system(count_reads_peaks_str)