#!/bin/bash

# Run this script to filter VCF files that have been created by merging indidual family member VCFs
# It should be run from the directory containing gzipped merged VCFs
# Make sure the GATK module is loaded



for file in *.gz

do
	# Get the family ID
	famID=${file%%.*} 
	
	# Remove variant sites at the unlocalized contigs (those with the GL00.... naming convention)
	# These would eventually be ignored anyway, so it'd be better to remove them now to speed the following steps up.

	zcat $file | grep -v GL0 > "${famID}".merged.noGL0
 
	# filter out variants that aren't SNPs or don't "PASS" VQSR
	# using "stdout" allows the vcftools command to be piped to another command or have the output written to a file
	
	vcftools --vcf "${famID}".merged.noGL0 --remove-indels --remove-filtered-all --recode --recode-INFO-all --stdout > "${famID}".merged.noGL0.SnpsOnly.PassVQSR 
		
	# Deleting the intermediate files as soon as they're no longer needed in the pipeline.
	rm "${famID}".merged.noGL0

	# GATK's VariantFiltration tool doesn't accept gzipped files as input	
	# VCFtools is not used here because it will replace a GQ or DP that is to be filtered out with a missing value character (".") whereas GATK will tag them with "low" which can then be referenced in order to remove them.
	# The $EBROOTGATK/GenomeAnalysisTK.jar references GATK when the module is loaded. Otherwise that would be replaced with the path to GATK.
	# /usr/bin/time -v will output memory usage and time.  This caused a problem when used with vcftools for some reason, but vcftools creates it's own log named "out.log"	
	# |$ tee will output progress to StdOut and StdErr, and write to file. Only the two GATK steps are being logged.
	
	/usr/bin/time -v java -jar $EBROOTGATK/GenomeAnalysisTK.jar -T VariantFiltration -R ~/1000genomes/human_g1k_v37.fasta -V:VCF "${famID}".merged.noGL0.SnpsOnly.PassVQSR -G_filter "GQ < 30.0 || DP < 10.0" -G_filterName low -U ALLOW_SEQ_DICT_INCOMPATIBILITY -o "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP |& tee "${famID}".filtering.log
	
	rm "${famID}".merged.noGL0.SnpsOnly.PassVQSR
	rm "${famID}".merged.noGL0.SnpsOnly.PassVQSR.idx
	
	# Filter out low GQ and DP variants based on the tags that were previously added by GATK	
	grep -v low "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP > "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP.LowGQandDPfilteredOut

	rm "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP
	rm "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP.idx
	
	# This script will read the VCF and only retain sites at which the probrand has at least one alternate allele and the other three family members have no variant called
	# This will output a file with the extension ".denovo" added to the input file name
	python ~/MergedVCFs/find-denovo.py "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP.LowGQandDPfilteredOut dad mom sibling proband

	rm "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP.LowGQandDPfilteredOut

	# Variants are annotated with known rsIDs
	# Multithreading can be used at this step. Currently it will run on 8 threads (-nt 8)	
	/usr/bin/time -v java -jar $EBROOTGATK/GenomeAnalysisTK.jar -T VariantAnnotator -nt 8 -U ALLOW_SEQ_DICT_INCOMPATIBILITY -R ~/1000genomes/human_g1k_v37.fasta -V:VCF "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP.LowGQandDPfilteredOut.denovo --dbsnp /data/dbSNP/b150/00-All.vcf.gz -o "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP.LowGQandDPfilteredOut.denovo.rsIDs |& tee -a "${famID}".filtering.log
	
	rm "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP.LowGQandDPfilteredOut.denovo
	rm "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP.LowGQandDPfilteredOut.denovo.idx
	
	# Filter out variants with known rsIDs in order to retain only the less common variants
	# /#/ tells awk to keep lines with the # character in them, otherwise the header lines are removed
	awk '/#/ || $3=="." {print $0}' "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP.LowGQandDPfilteredOut.denovo.rsIDs > "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP.LowGQandDPfilteredOut.denovo.rsIDs.rsIDsFilteredOut
	
	rm "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP.LowGQandDPfilteredOut.denovo.rsIDs
	rm "${famID}".merged.noGL0.SnpsOnly.PassVQSR.TaggedLowGQandDP.LowGQandDPfilteredOut.denovo.rsIDs.idx

done	
