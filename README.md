[![Docker](https://img.shields.io/docker/pulls/y9ch/sacseq.svg)](https://hub.docker.com/r/y9ch/sacseq)

# m6A-SAC-seq

## Overview of the workflow

## How to use?

For reproducibility, source code and dependencies have been packaged into one [docker image](https://hub.docker.com/r/y9ch/sacseq).

You can run it thought [singularity](https://sylabs.io/singularity) container runtime.

- Specific the path and the label of your data a yaml file:

for example,

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

- Then run all the analysis by one command:

```bash
singularity exec docker://y9ch/sacseq:latest sacseq data.yaml
```

## Documentation

https://github.com/y9c/m6A-SACseq/wiki

## Citation

- (nbt)
