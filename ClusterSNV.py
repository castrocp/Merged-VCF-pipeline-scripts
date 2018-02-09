#!/usr/bin/env python

# This will run a 100-base-pair sliding window through the list of candidate denovo SNVs to determine which of them are within 100bps of each other.

import sys


def main():

	winSize = int(raw_input("How many base-pairs in size do you want the bins to be? "))
	inFileName = sys.argv[1]

	with open (inFileName) as infile:
		with open ('CandidatedDenovosClustered', "w") as outfile:
			outfile.write("Chrom" + "\t" + "start" + "\t" + "end" + "\t" + "ref" + "\t" + "alt" + "\t" + "geno" + "\t" + "famID" + "\t" + "regDB" + "\t" + "b_start" + "\t" + "b_end" + "\t" + "b_population" + "\n")
			# Write a header to the ouput file
			
			while True:
				line = infile.readline()
				if not line: break
			# Need to run everything after this line of code for each line of the file
			# Each line of the file represents a variant, and there will be a bin for each variant	
				
				bin_pop = 1
				# To keep track of how many variants are found within each bin
				
				(chrom, start, end, ref, alt, geno, famID, regdb) = line.strip("\n").split()
				# This is the line format in the candidate denovos file after the RegDB annotation step  
				
				start_bin = int(start)
				# The coordinates in the input file are 0-based. I'm using the start coordinate to mark the start of a variant's bin
					
				end_bin = start
				# If no other variant is added to the bin, the bin starts and ends at the same point. Otherwise, the ending point is updated. 		
				current_line_pointer = infile.tell()
				# This variable saves the location of the pointer so we can go back to this line position
				# The pointer is at the end of the line that was just read and parsed
				
				try:
					next_variant_pos = int(infile.readline().strip("\n").split()[1])
				except:
					break
				# This is a shortened version of the parsing I did above. 
				# Index "1" points to the "start" coordinate of the variant on the next line

				while next_variant_pos - start_bin <= winSize:
					bin_pop += 1
					# Keeps track of additional variants that fall within the bin
					end_bin = next_variant_pos
					# Updates the end coordinate of the bin
					try:			
						next_variant_pos = int(infile.readline().strip("\n").split()[1])
					# Keeps moving to the next line of the input file to compare the next variant to the current start_bin coordinate
					except:
						break
						
	
				# Once the next variant no longer falls within the bin, exit the loop, write to the output file
				outfile.write(line.strip("\n") + "\t" + str(start_bin) + "\t" + str(end_bin) + "\t" + str(bin_pop) + "\n")

				infile.seek(current_line_pointer)
				# Set the pointer back to the line the bin started at so that it's ready to loop to the next line in order


if __name__ == '__main__':
	main() 

 
