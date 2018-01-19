#!/usr/bin/env python3

import sys


'''
Script will read a file that has been annotated by RegulomeDB and scored, and filter out 
unwanted scores.  Output file will only contain the positions with desired scores.

run program as:
filterRegDBscore.py <name of scored file to filter>
'''

def main():

    inFileName = sys.argv[1]

    WantedScores = ["1a","1b","1c","1d","1e","1f","2a","2b","2c","3a","3b"]

    with open (inFileName, 'r') as infile:  #when you use "with open" you don't have to close the file later
    	with open (inFileName + ".filteredScores", "w") as filteredscores: 
            for line in infile:
            	(chrom, start, end, refAllele, altAllele, probandGT, familyID, data, score)= line.strip("\n").split("\t")
            	if score in WantedScores:
            		filteredscores.write("chr"+chrom + "\t" + start + "\t" + end + "\t" + refAllele + "\t" + altAllele + "\t" + probandGT + "\t" + familyID + "\t" + score + "\n")
		# Coordinates will be 0-based since the input file was 0-based

if __name__ == '__main__':
    main()
            	


    
