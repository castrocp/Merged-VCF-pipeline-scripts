#!/bin/bash

# Convert a VCF file into BED format and annotate with RegulomeDB

# A link to the hash table needs to be created in whatever directory the files to be annotated are in
ln -s /data/RegulomeDB/WWW/RegulomeDB/data/RegulomeDB/mapPWMtoHUGO.hash

for file in *.rsIDsFilteredOut

do

	python ~/MergedVCFs/convert2bed.py $file
	# This script will convert the VCF file into BED format, creating a new file with the ".bed" extension, with 7 columns:
	# chrom, start, end, ref allele, alt allele, proband genotype, family ID

	~/LocalRegDBquery/RegDB_query.pl ${file}.bed /data/RegulomeDB/WWW/RegulomeDB/data/RegulomeDB > ${file}.regDBannotated.bed 

done
