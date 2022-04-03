#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2021 Ye Chang yech1990@gmail.com
# Distributed under terms of the MIT license.
#
# Created: 2021-11-12 19:54

"""realign bam file by python."""

import re
import sys

import pysam

re_split_md = re.compile(r"[\^ATGC]+|\d+")


def find_clip(alignment, mm=5):
    """find clip on both end."""

    def clip_alignment(alignment, mm):
        n_clip = 0
        n_match = 0
        for qp, rp, rb in alignment:
            if n_match >= mm:
                break
            if rb and rb in "ACGT" and rp is not None and qp is not None:
                n_match += 1
            else:
                n_match = 0
            n_clip += 1
        return n_clip - mm

    return clip_alignment(alignment, mm), clip_alignment(alignment[::-1], mm)


def clip_cigar(cigartuples, n_clip):
    # M	BAM_CMATCH	0
    # I	BAM_CINS	1
    # D	BAM_CDEL	2
    # N	BAM_CREF_SKIP	3
    # S	BAM_CSOFT_CLIP	4
    # H	BAM_CHARD_CLIP	5
    # P	BAM_CPAD	6
    # =	BAM_CEQUAL	7
    # X	BAM_CDIFF	8
    # B	BAM_CBACK	9
    if n_clip > 0:
        n_cigar = 0
        n_len = 0
        for i, (t, n) in enumerate(cigartuples):
            n_cigar += n
            if n_cigar > n_clip:
                break
            n_len += n
        if t != 4:
            new_cigar = [
                (4, n_clip),
                (t, n - n_clip + n_len),
            ] + cigartuples[i + 1 :]
        else:
            new_cigar = [(4, n + n_len)] + cigartuples[i + 1 :]
        return new_cigar
    return cigartuples


def alignment_to_md(alignment):
    status = []
    bases = []
    for qp, rp, rb in alignment:
        if qp is None:
            status.append("I")
            bases.append(rb.upper())
        elif rb and rb.islower():
            status.append("X")
            bases.append(rb.upper())
        else:
            status.append("=")
            bases.append(1)

    md = ""
    s_pre = ""
    n_match = 0

    for s, b in zip(status, bases):
        if s == "=":
            n_match += 1
        elif s == "I":
            if s_pre != "I":
                md += str(n_match) + "^" + b
                n_match = 0
            else:
                md += "^" + b
        elif s == "X":
            if s_pre != "X":
                md += str(n_match) + b
                n_match = 0
            else:
                md += b
        s_pre = s
    md += str(n_match)

    return md


if __name__ == "__main__":
    input_fa_name = "/home/yec/reference/genome/Homo_sapiens.GRCh38.rRNA.fa"
    input_sam_name = "./test.bam"
    output_bam_name = "-"

    # input_fa_name = sys.argv[1]
    # input_sam_name = sys.argv[2]
    # output_bam_name = sys.argv[3]

    fafile = pysam.FastaFile(input_fa_name)
    samfile = pysam.AlignmentFile(input_sam_name, "r")
    outfile = pysam.AlignmentFile(output_bam_name, "w", template=samfile)

    pad = 20
    for read in samfile.fetch():
        if (
            (
                "D" in read.cigarstring
                or "S" in read.cigarstring
                or not read.get_tag("MD").isnumeric()
            )
            and read.reference_name in fafile.references
            # TODO: support realign splicing reads
            and "N" not in read.cigarstring
        ):
            outfile.write(read)
            alignment = read.get_aligned_pairs(with_seq=True)
            l_clip, r_clip = find_clip(alignment, mm=5)
            read.cigartuples = clip_cigar(read.cigartuples, l_clip)
            read.cigartuples = clip_cigar(read.cigartuples[::-1], r_clip)[::-1]
            new_md = alignment_to_md(alignment[l_clip : len(alignment) - r_clip])
            read.set_tag("MD", new_md)
            outfile.write(read)
