#!/usr/bin/env python3

import sys

import numpy as np
import pandas as pd

# files = [
#     "../workspace_HGS_mouse/compute_matrix/HGS3-mgDNA1.gz",
#     "../workspace_HGS_mouse/compute_matrix/HGS3-mgDNA2.gz",
# ]
files = sys.argv[1:]
dfs = []
for f in files:
    n = f.split("/")[-1].split(".")[0]
    df = (
        pd.read_csv(
            f,
            sep="\t",
            comment="@",
            names=[f"V{i}" for i in range(1, 1101, 1)],
            usecols=np.arange(6, 1106, 1),
        )
        .mean()
        .rename(n)
    )
    dfs.append(df)

pd.concat(dfs, axis=1).to_csv(sys.stdout, sep="\t", index=False)
