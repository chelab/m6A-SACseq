---
title: Run the pipeline
nav_exclude: false
---

<!-- prettier-ignore-start -->
# Run the pipeline
{: .fs-9 }
<!-- prettier-ignore-end -->

Step by Step Instruction
{: .fs-6 .fw-300 }

## Prepare references

data
{: .label .label-green }

- download fasta

```bash
wget ....
```

- build index

```bash
bowtie2 ....
```

## Refer rawdata and references in the configuration file

configuration
{: .label .label-blue }

{: .note }
How to refer the rawdata in the YAML file?

The rawdata can be defined under the `samples` config group.

```yaml
samples:
  { <code>REPLACE_WITH_YOUR_GROUP_ID</code> }:
    { <code>input</code> | <code>treated</code> }:
      { <code>REPLACE_WITH_YOUR_SAMPLE_ID</code> }:
        - R1: <code>file path</code>
          R2: <code>file path</code>
```

- The 1st level is the `samples` tag.
- The 2nd level is the `{GROUP_ID}` tag.
  You can classify your samples into different groups, and the label `{GROUP_ID}` can be customized. For example, you can have a `HeLa-WT` and a `HeLa-KO` group for different data. These labels will be used to name the intermediate and final results of the analysis.
- The 3rd level should be one of `input` or `treated` tag.
  The data under the `treated` tag will be used for m<sup>6</sup>A site detected. And data under the `input` tag will be used for SNP / FP (false positive) sites removal.
- The 4th level is the `{SAMPLE_ID}` tag.
  Since you can have multiple replicates in the experiment design, the `{SAMPLE_ID}` can be `rep1`, `rep2`, `rep3`... or some other uniuqe labels.
- The 5th level is a **list** of paired sequencing data.
  Read1 and Read2 are labeled after `R1` and `R2` respectively.
  Note that this level is a list instead of a single value, so you can group multiple sequencing runs together, and the pipeline will automatically combine the data for the same library.
  In addition, if you add new sequencing data for your library, you can append a new record to the list. After that, the pipeline will automatically re-run some of the steps with **only the new data**, saving computation resources.

All levels can have multiple records. Such as the example below.

```yaml
samples:
  HeLa-WT:
    input:
      rep1:
        - R1: ./rawdata/HeLa-WT-input-rep1-run1_R1.fq.gz
          R2: ./rawdata/HeLa-WT-input-rep1-run1_R2.fq.gz
        - R1: ./rawdata/HeLa-WT-input-rep1-run2_R1.fq.gz
          R2: ./rawdata/HeLa-WT-input-rep1-run2_R2.fq.gz
        - R1: ./rawdata/HeLa-WT-input-rep1-run3_R1.fq.gz
          R2: ./rawdata/HeLa-WT-input-rep1-run3_R2.fq.gz
      rep2:
        - R1: ./rawdata/HeLa-WT-input-rep2-run1_R1.fq.gz
          R2: ./rawdata/HeLa-WT-input-rep2-run1_R2.fq.gz
    treated:
      rep1:
        - R1: ./rawdata/HeLa-WT-treat-rep1-run1_R1.fq.gz
          R2: ./rawdata/HeLa-WT-treat-rep1-run1_R2.fq.gz
        - R1: ./rawdata/HeLa-WT-treat-rep1-run2_R1.fq.gz
          R2: ./rawdata/HeLa-WT-treat-rep1-run2_R2.fq.gz
        - R1: ./rawdata/HeLa-WT-treat-rep1-run3_R1.fq.gz
          R2: ./rawdata/HeLa-WT-treat-rep1-run3_R2.fq.gz
      rep2:
        - R1: ./rawdata/HeLa-WT-treat-rep2-run1_R1.fq.gz
          R2: ./rawdata/HeLa-WT-treat-rep2-run1_R2.fq.gz
  HeLa-KO:
    input:
      rep1:
        - R1: ./rawdata/HeLa-KO-input-rep1-run1_R1.fq.gz
          R2: ./rawdata/HeLa-KO-input-rep1-run1_R2.fq.gz
    treated:
      rep1:
        - R1: ./rawdata/HeLa-KO-treat-rep1-run1_R1.fq.gz
          R2: ./rawdata/HeLa-KO-treat-rep1-run1_R2.fq.gz
```

_NOTE: in the example, there are 2 replicates for HeLa-WT. For HeLa-WT (input/treated) rep1 library, there are 3 sequencing run. Data for the sample library will be combined for analysis._

{: .note }
How to refer the reference/index in the YAML file?

Such as the example below.

```yaml
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

## Customized analysis parameters

configuration
{: .label .label-blue }

- threads

```yaml
jobs: 48
```

- output (workdir)

```yaml
workdir: ./results
```

## Run the pipeline

- How to use singularity?
- HPC envirentment
