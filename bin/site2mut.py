#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2022 Ye Chang yech1990@gmail.com
# Distributed under terms of the GNU license.
#
# Created: 2022-04-03 02:14


import sys

import pyensembl
import varcode
from pyfaidx import Fasta

# ensembl_genome = pyensembl.Genome(
#     reference_name="TAIR10",
#     annotation_name="Arabidopsis_thaliana",
#     gtf_path_or_url="/home/yec/reference/feature/Arabidopsis_thaliana.TAIR10.genome.gtf",
#     transcript_fasta_paths_or_urls="/home/yec/reference/cdna/Arabidopsis_thaliana.TAIR10.cdna.all.fa.gz",
#     protein_fasta_paths_or_urls="/home/yec/reference/protein/Arabidopsis_thaliana.TAIR10.pep.all.fa.gz",
# )


def site2mut(chrom, pos, base, genome):
    """return.

    - mut_type
    - eff.gene_name
    - transcript_id
    - transcript_pos
    - transcript_motif
    - coding_pos
    - codon_ref
    - aa_pos
    - aa_ref
    """
    pad = 10

    chrom = str(chrom)
    if chrom not in genome.contigs():
        return [None] * 9
    effs = varcode.EffectCollection(
        [
            e
            for b in "ATGC"
            if b != base
            for e in varcode.Variant(
                contig=chrom, start=pos, ref=base, alt=b, ensembl=genome
            ).effects()
        ]
    )

    eff = effs.top_priority_effect()
    mut_type = type(eff).__name__
    transcript_id = None if mut_type == "Intergenic" else eff.transcript_id

    non_exon_recored = [mut_type, eff.gene_name, transcript_id] + [None] * 6
    if mut_type in ["Intergenic", "Intronic", "SpliceDonor"]:
        return non_exon_recored
    try:
        transcript_pos = eff.transcript.spliced_offset(pos) + 1
    except:
        return non_exon_recored
    # transcript motif
    s = eff.transcript.sequence
    if s is not None:
        s5 = (s[max(transcript_pos - 1 - pad, 0) : transcript_pos - 1]).rjust(
            pad, "N"
        )
        s0 = s[transcript_pos - 1]
        s3 = (s[transcript_pos : transcript_pos + pad]).ljust(pad, "N")
        transcript_motif = s5 + s0 + s3
    else:
        transcript_motif = None
    # codon
    if (
        mut_type not in ["NoncodingTranscript", "IncompleteTranscript"]
        and eff.transcript.first_start_codon_spliced_offset
        <= transcript_pos - 1
        <= eff.transcript.last_stop_codon_spliced_offset
    ):
        coding_pos = (
            transcript_pos - eff.transcript.first_start_codon_spliced_offset
        )
        codon_start = (coding_pos - 1) // 3 * 3
        codon_ref = eff.transcript.coding_sequence[
            codon_start : codon_start + 3
        ]
    else:
        coding_pos = None
        codon_ref = None

    if mut_type == "Silent":
        aa_pos_offset = eff.aa_pos
        aa_ref = eff.aa_ref if coding_pos else None
    elif mut_type in ["IntronicSpliceSite", "ExonicSpliceSite"]:
        aa_pos_offset = eff.alternate_effect.aa_pos
        aa_ref = eff.alternate_effect.aa_ref if coding_pos else None
    elif mut_type == "StopLoss":
        aa_pos_offset = eff.aa_mutation_start_offset
        aa_ref = "*"
    else:
        aa_pos_offset = eff.aa_mutation_start_offset
        aa_ref = eff.aa_ref if coding_pos else None
    if aa_ref == "":
        aa_ref = None
    aa_pos = int(aa_pos_offset) + 1 if coding_pos else None

    return [
        mut_type,
        eff.gene_name,
        transcript_id,
        transcript_pos,
        transcript_motif,
        coding_pos,
        codon_ref,
        aa_pos,
        aa_ref,
    ]


# print(site2mut("1", 31644844, "C", ensembl_genome))

# with open("../note/HepG2_sites_for_validation.tsv", "r") as f:
if __name__ == "__main__":

    RC_dict = dict(zip("ACGTNacgtn", "TGCANtgcan"))
    ensembl_fasta = Fasta(
        "/home/yec/reference/genome/Homo_sapiens.GRCh38.genome.fa"
        # "/home/yec/reference/genome/hg38.fa"
    )

    ensembl_genome = pyensembl.EnsemblRelease(
        release="102", species="homo_sapiens"
    )

    ensembl_genome.index()

    with open(sys.argv[1], "r") as f:
        for l in f:
            c, p, s, *_ = l.strip().split("\t")
            b = ensembl_fasta[c][int(p) - 1].seq
            # if s == "-":
            #    b = RC_dict[b]
            print(
                l.strip("\n")
                + "\t"
                + "\t".join(
                    map(
                        str,
                        site2mut(
                            c.replace("chr", ""), int(p), b, ensembl_genome
                        ),
                    )
                )
            )
