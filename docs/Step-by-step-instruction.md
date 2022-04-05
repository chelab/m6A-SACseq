---
title: Step by Step Instruction
nav_exclude: false
---

<!-- prettier-ignore-start -->
# Step by Step Instruction
{: .fs-9 }
<!-- prettier-ignore-end -->

## Prepare references

data
{: .label .label-green }

- download fasta
- build index

## Refer rawdata and references in the configuration file

configuration
{: .label .label-green }

```markdown
{: .note }
How to refer the rawdata in the YAML file?
```

The rawdata can be defined under the `samples` config group.

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

```markdown
{: .note }
How to refer the reference/index in the YAML file?
```

## Customized analysis parameters

configuration
{: .label .label-green }

- threads
- output (workdir)
