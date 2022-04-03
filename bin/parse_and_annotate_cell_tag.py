#!/usr/bin/env python3

import sys

import pysam

# barcode_file = "../note/bc_mapping.tsv"
# input_file_name = "../workspace_sc_plate/drop_duplicates/HeLa-sc-plate-condition1-treated_genome.bam"
# output_file_name = "test.bam"
barcode_file = sys.argv[1]
input_file_name = sys.argv[2]
output_file_name = sys.argv[3]

plate_name = "P01"
with open(barcode_file) as f:
    barcode_dict = {line.split()[1]: plate_name + line.split()[0] for line in f}

input_file = pysam.AlignmentFile(
    input_file_name,
    "rb",
)
output_file = pysam.AlignmentFile(
    output_file_name,
    "wb",
    template=input_file,
)

for read in input_file.fetch():
    cell_barcode = read.query_name.rsplit("_", 1)[1][:6]
    read.set_tag("XC", barcode_dict.get(cell_barcode))
    if read.has_tag("XC"):
        output_file.write(read)

output_file.close()
input_file.close()
