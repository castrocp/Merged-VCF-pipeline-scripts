#!/usr/bin/env python

# Read a BED file with SNV coordinates and output a file with a columnn giving the distance between the current SNV and the following SNV

# Run as:  SNVdistance.py inFileName
# Excpects the input file to be in the format of the clustered file created with ClusterSNV.py
# This won't work if there's a header on the file, so use a no-header version


import sys


def main():

	inFileName = sys.argv[1]

	with open (inFileName) as infile:
		with open (inFileName + '.SNVdistances', "w") as outfile:
			outfile.write("Chrom" + "\t" + "start" + "\t" + "end" + "\t" + "ref" + "\t" + "alt" + "\t" + "geno" + "\t" + "famID" + "\t" + "regDB" + "\t" + "b_start" + "\t" + "b_end" + "\t" + "b_population" + "\t" + "dist_to_next_snv" + "\n")
			# Write a header to the ouput file
			
			while True:
				line = infile.readline()
				if not line: break
			# Need to run everything after this line of code for each line of the file
			# Each line of the file represents a variant
				
				(chrom, start, end, ref, alt, geno, famID, regdb, bin_start, bin_end, bin_pop) = line.strip("\n").split()
				# This is the line format in the clustered candidate denovos file after running ClusterSNV.py   
				
				current_variant_pos = int(start)
	
				current_line_pointer = infile.tell()
				# This variable saves the location of the pointer so we can go back to this line position
				# The pointer is at the end of the line that was just read and parsed
				
				try:
					next_variant_pos = int(infile.readline().strip("\n").split()[1])
					# This is a shortened version of the parsing I did above.
					# Index "1" points to the "start" coordinate of the variant on the next line
				except:
					outfile.write(line.strip("\n") + "\t" + str("0") + "\n")
					break
					# This will only occur when the last line of the input file is being processed
					# Since there is no next line to read, it will just write the last entry to the outfile and finish				
				
				dist_to_next = next_variant_pos - current_variant_pos
				
				if dist_to_next > -1:
				# The distance will be positive unless you're comparing coordinates between chromosomes
					outfile.write(line.strip("\n") + "\t" + str(dist_to_next) + "\n")
				else:
					outfile.write(line.strip("\n") + "\t" + str("0") + "\n")
					# Just write a distance of "0" if the next variant falls in the next chromosome

				infile.seek(current_line_pointer)
				# Set the pointer back to the line we started at so that it's ready to loop to the next line in order


if __name__ == '__main__':
	main() 

 
