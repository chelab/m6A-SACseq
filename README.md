[![Docker](https://img.shields.io/docker/pulls/y9ch/sacseq.svg)](https://hub.docker.com/r/y9ch/sacseq)

# m6A-SAC-seq

## Overview of the workflow

### Quality control:

We will first perform read trimming to remove adapter, primer sequences, molecular barcode (UMI) and low quality bases using cutadapt software.

### Data Processing:

All trimmed reads will be mapped to E. coli and Mycoplasma genome to filter biological contamination RNA using the bowtie2 tool, and then unmapped reads will be mapped to spike-in sequence to filter RNA spike-in. Similarly, unmapped reads will be mapped to the ribosomal RNA, small RNA and mRNA (whole genome) reference sequence sequentially. After mapping, reads with identical UMI and mapped to the same location will be treated as PCR duplicates and dropped from downstream analysis.

### m6A Analyses:

m6A sites (mutation signal) were detected simultaneously, and mutation number and sequencing depth for each mutation position among all the samples were recorded. Then putative m6A sites will be detected based on the mutation ratio, mutation number and sequencing depth of each mutation position.

## How to use?

For reproducibility, source code and dependencies have been packaged into one [docker image](https://hub.docker.com/r/y9ch/sacseq). You can run it thought [singularity](https://sylabs.io/singularity) container runtime.

It would be very simple to finish the whole analysis. Just 3 steps:

1. **Specific the path (with label) of both rawdata and references for your project in a YAML format.** For example,

<details>
  <summary>Save the following config into <code>data.yaml</code> file. <sup>(Click to expand)</sup></summary>
  
```yaml
samples:
  HeLa-WT:
    input:
      rep1:
        - R1: ./rawdata/HeLa-WT-polyA-input-rep1-run1_R1.fq.gz
          R2: ./rawdata/HeLa-WT-polyA-input-rep1-run1_R2.fq.gz
        - R1: ./rawdata/HeLa-WT-polyA-input-rep1-run2_R1.fq.gz
          R2: ./rawdata/HeLa-WT-polyA-input-rep1-run2_R2.fq.gz
      rep2:
        - R1: ./rawdata/HeLa-WT-polyA-input-rep2-run1_R1.fq.gz
          R2: ./rawdata/HeLa-WT-polyA-input-rep2-run1_R2.fq.gz
        - R1: ./rawdata/HeLa-WT-polyA-input-rep2-run2_R1.fq.gz
          R2: ./rawdata/HeLa-WT-polyA-input-rep2-run2_R2.fq.gz
    treated:
      rep1:
        - R1: ./rawdata/HeLa-WT-polyA-treated-rep1-run1_R1.fq.gz
          R2: ./rawdata/HeLa-WT-polyA-treated-rep1-run1_R2.fq.gz
        - R1: ./rawdata/HeLa-WT-polyA-treated-rep1-run2_R1.fq.gz
          R2: ./rawdata/HeLa-WT-polyA-treated-rep1-run2_R2.fq.gz
      rep2:
        - R1: ./rawdata/HeLa-WT-polyA-treated-rep2-run1_R1.fq.gz
          R2: ./rawdata/HeLa-WT-polyA-treated-rep2-run1_R2.fq.gz
        - R1: ./rawdata/HeLa-WT-polyA-treated-rep2-run2_R1.fq.gz
          R2: ./rawdata/HeLa-WT-polyA-treated-rep2-run2_R2.fq.gz
references:
  spike:
    fa: ./ref/spike-in.fa
    bt2: ./ref/spike-in.fa
  spikeN:
    blast: ./ref/spike-in_with_N
  rRNA:
    fa: ./ref/Homo_sapiens.GRCh38.rRNA.fa
    bt2: ./ref/Homo_sapiens.GRCh38.rRNA
  smallRNA:
    fa: ./ref/Homo_sapiens.GRCh38.smallRNA.fa
    bt2: ./ref/Homo_sapiens.GRCh38.smallRNA
  genome:
    fa: ./ref/Homo_sapiens.GRCh38.genome.fa
    star: ./ref/Homo_sapiens.GRCh38.genome
    gtf: ./ref/Homo_sapiens.GRCh38.genome.gtf
    fai: ./ref/Homo_sapiens.GRCh38.genome.fa.fai
    gtf_collapse: ./ref/Homo_sapiens.GRCh38.genome.collapse.gtf
  contamination:
    fa: ./ref/contamination.fa
    bt2: ./ref/contamination
```

</details>

2. **Run all the analysis by one command**:

```bash
singularity exec docker://y9ch/sacseq:latest sacseq data.yaml
```

3. **View the analysic report (`./results/report.html`) and use the m6A sites for downstream analysis**.

## Documentation

https://github.com/y9c/m6A-SACseq/wiki

## Citation

- Hu, L., Liu, S., Peng, Y. et al. m6A RNA modifications are measured at single-base resolution across the mammalian transcriptome. Nat Biotechnol (2022). https://doi.org/10.1038/s41587-022-01243-z
