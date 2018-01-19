#!/usr/bin/env python

from __future__ import print_function
import sys
import re
import gzip

# run program as:
# find-denovo.py <VCFfilename>  <first person> <second person> <third person> <fourth person>
# (type "mom","dad", "proband", or "sibling")
# type them in the order of their respective VCF columns.  If sibling comes first in the VCF, type "dad mom sibling proband"
# This script will look for instances in which the proband's genotype is displayed, and the other 3 family members' genotypes are missing.  This will show up as "." and implies that they are homozygous reference.

def main():
    inFileName = sys.argv[1]
    momIdx = sys.argv.index("mom")  #user inputs the order of the family member columns
    dadIdx = sys.argv.index("dad")
    childIdx = sys.argv.index("proband")
    siblingIdx = sys.argv.index("sibling")

    with open (inFileName, 'r') as infile: # gzip.open (inFileName, 'r') as infile:  #when you use "with open" you don't have to close the file later
            with open (inFileName + ".denovo", "w") as variantFile: 
            	for line in infile:
			if line.startswith("#"):   # header and info lines start with "#"
                            variantFile.write(line) 
			else:
                		is_denovo_variant = process_line(line, momIdx-2, dadIdx-2, childIdx-2, siblingIdx-2)
				
				if is_denovo_variant == True:
                        		variantFile.write(line) 
			
def process_line(line, momIdx, dadIdx, childIdx, siblingIdx):
        is_denovo_variant = False

        (chrom, pos, ID, ref, alt, qual, Filter, info, format, samples) = line.strip("\n").split("\t", 9)
        samples = samples.split("\t")
     	
	dadgeno = samples[dadIdx]
	momgeno = samples[momIdx]
        childgeno = samples[childIdx]
	siblinggeno = samples[siblingIdx]
        
	dadAlleles = extract_genes(dadgeno)
	momAlleles = extract_genes(momgeno)
	childAlleles = extract_genes(childgeno)
	siblingAlleles = extract_genes(siblinggeno)
	
	if dadAlleles == "." and momAlleles == "." and siblingAlleles == ".":
		is_denovo_variant = True
	
	return(is_denovo_variant)

def extract_genes(unparsed_geno):
        # split the data by ":", to access only the genotype
        # first element of the list is the genotype when format is Genotype:Quality:ReadDepth:etc.
        geno = unparsed_geno.split(":")[0]

        # split the genotypes into individual alleles - split on "/" or "|"
        #alleles = re.split(r"/|\|", geno)

        return geno #alleles

if __name__ == '__main__':
        main()

