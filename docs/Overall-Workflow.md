---
title: Overall Workflow
parent: Introduction
has_children: true
nav_order: 1
---

# Overall Workflow
{: .fs-9 }

![pipeline](pipeline.png)

## Quality control:

We will first perform read trimming to remove adapters, primer sequences, molecular barcode (UMI), and low-quality bases using the `cutadapt` software.

## Data Processing:

All trimmed reads will be mapped to E. coli and Mycoplasma genome to filter biological contamination RNA using the bowtie2 tool, and then unmapped reads will be mapped to spike-in sequence to filter RNA spike-in. Similarly, unmapped reads will be mapped to the ribosomal RNA, small RNA and mRNA (whole genome) reference sequence sequentially. After mapping, reads with identical UMI and mapped to the same location will be treated as PCR duplicates and dropped from downstream analysis.

## m6A Analyses:

m6A sites (mutation signal) were detected simultaneously, and mutation number and sequencing depth for each mutation position among all the samples were recorded. Then putative m6A sites will be detected based on the mutation ratio, mutation number, and sequencing depth of each mutation position.
