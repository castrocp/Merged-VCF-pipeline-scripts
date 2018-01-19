#!/usr/bin/env python3
import sys

'''
Script will convert a found-variant file to BED format.

run program as:
convert2bed.py <name of file to convert to BED format>

The script assumes the file naming format is "FamilyID.blahblahb" with the ID being first and followed by a period

Currently being applied to a 13-column VCF file filtered down to candidate de novo SNVs
1st column needs "chr" added to the chromosome number since the regulomeDB query script required that format.
Position needs to be listed as start-end in 0-based coordinates, per BED format rules
VCF coordinates are 1-based, so each position from the VCF file needs to have 1 base subracted when converted to BED format
'''

def main():
	
    inFileName = sys.argv[1]
    
    with open (inFileName, 'r') as infile:
        familyID=inFileName.split(".")[0]
        with open (inFileName + ".bed", "w") as Bed:
            for line in infile:
                if not line.startswith("#"):
		# skip the header lines	
			(chrom, pos, id, ref, alt, qual, filt, info, format, Fgt, Mgt, Sgt, Pgt)= line.strip("\n").split()
			probandGT = Pgt.split(":")[0] 
			# Since these are candidate de novo variants, it is assumed the father, mother, sibling genotypes are all homozygous reference
                	Bed.write("chr"+chrom + "\t" + str(int(pos)-1) + "\t" + pos + "\t" + ref + "\t" + alt + "\t" + probandGT + "\t" + familyID + "\n") 
           		#BED format is zero-based; VCF is 1-based
           		#So, BED start coordinate is one less than VCF start.

if __name__ == '__main__':
    main()
            	
