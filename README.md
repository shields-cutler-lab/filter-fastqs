# Helper scripts to filter fastq files based on alignments

### Given a BLAST output table format 6 (.b6), filters aligned reads from the fastq file.

In certain cases, one needs to remove reads from a fastq file before analysis (e.g. contamination) or before sharing (e.g. removing human-source metagenomic reads before depositing in a public database). To identify unwanted reads, the processed reads should be aligned to an appropriate database (an "exclusion" database). These scripts were designed with alignments using the BURST optimal aligner. See [the BURST repo](https://github.com/knights-lab/BURST) for more information. When aligned to a database based on the human genome, for example, all reads in the resulting b6 file are assumed to be of human origin. These scripts read the b6 file and the original fastq, and output a filtered fastq.

One script processes single end (SE) reads; the other processes paired end (pe) reads. In the latter, the union of R1 and R2 hits are recorded and removed. That is to say that even if only R2 positively aligns with the exclusion database, the read pair is removed in entirety. This way, downstream stitching and other paired-end methods are protected. 

### Dependencies
Requires BioPython. Easy installation with conda:
```conda install -c conda-forge biopython```

### Single-end usage
```python
python filter_SE_fq_b6.py alignment.b6 original.fastq filtered_filename summary_fname/NONE summary_dir/NONE
````
'filtered_filename' is the prefix for the .fastq output file. `summary_fname` is the prefix for a .txt file, which will be saved in the `summary_dir` and lists the percent of reads that were filtered from the fastq.

### Paired-end usage
```python
python filter_by_b6.py align_R1.b6 align_R2.b6 orig_R1.fastq orig_R2.fastq filtered_prefix
```
Similar to above, the `filtered_prefix` here is the filename prefix for the output fastq.


### Example host filtering
Uses [SHI7](https://github.com/knights-lab/shi7) to pre-process the fastqs, and BURST to align.
```shell
####################################
###### Example host filtering ######
####################################

# Run SHI7 on the original fastq with a low quality threshold to retain the most possible host hits.
# Use 'combine_fasta False' to keep individual fasta files for each R1/R2.
shi7.py -i . -o qc_fasta/ --combine_fasta False --adaptor Nextera --flash False -trim_q 10 -filter_q 10

# For loop to process each fasta using burst. The exclusion database in this case is from a representative human genome.
# The 'ANY' mode in BURST will retain all hits above the given identity threshold, no breaking ties.
mkdir host_filter_b6
for f in qc_fasta/*.fna;
	do fname="${f%.*}";
	fname="$(basename $fname)";
	burst15 -r /project/flatiron2/sop/humanD252.edx -a /project/flatiron2/sop/humanD252.acx -q $f -o host_filter_b6/${fname}.b6 -n -m ANY -fr -i 0.98 -sa
done

mkdir host_filtered_fastq

for f in hf1_filter/*_R1.b6;
	do fname=$(basename $f);
	fname=${fname%_*};
	python filter_pe_fq_b6.py host_filter_b6/${fname}_R1.b6 host_filter_b6/${fname}_R2.b6 ${fname}_R1.fastq ${fname}_R2.fastq host_filtered_fastq/$fname;
	echo "finished a pair";
done
```