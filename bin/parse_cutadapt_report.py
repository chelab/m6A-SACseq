#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

# "../workspace_human_cellline/cut_adapter/HEK293-WT-polyA-input-rep1-run1_step1.report",
# "../workspace_human_cellline/cut_adapter/HEK293-WT-polyA-input-rep1-run1_step2.report",
files = sys.argv[1:]
counts = {"N": 0, "S": 0, "T": 0}
for i, fi in enumerate(files):
    if i % 2 == 0:
        c = []
    with open(fi, "r") as f:
        for line in f:
            # Do not use this regular expression, which is not support single end result
            # r1 = r"Total read pairs processed:\s+([0-9,]+)"
            # r2 = r"Pairs written \(passing filters\):\s+([0-9,]+)"
            r1 = r"Total read(?: pair)?s processed:\s+([0-9,]+)"
            r2 = r"(?:Reads|Pairs) written \(passing filters\):\s+([0-9,]+)"
            m1 = re.match(r1, line)
            if m1 is not None:
                c1 = int(m1.group(1).replace(",", ""))
            else:
                m2 = re.match(r2, line)
                if m2 is not None:
                    c2 = int(m2.group(1).replace(",", ""))
                    break
        c.append(c1)
        c.append(c2)
    if i % 2 == 1:
        counts["N"] += c[0] - c[1]
        counts["S"] += c[2] - c[3]
        counts["T"] += c[3]

print("NReads", counts["N"], sep="\t")
print("ShortReads", counts["S"], sep="\t")
print("FinalReads", counts["T"], sep="\t")
