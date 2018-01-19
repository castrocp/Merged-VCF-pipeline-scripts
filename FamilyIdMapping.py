#!/usr/bin/env python


# Use the family ID mapping file to create a text file for each family, listing the each family member's ID.

# IDs should be listed in the order of: father, mother, sibling, proband

# Run this from the command line as "python FamilyMemberIDFiles" from the same directory the "540families_idmapping" file is located in.  The output files will be created in the same directory.


def main():

	#Create dictionary to link individual family member ID to it's sample ID #
	#Create dictionary to link family ID without extension to a number counting the families
	FamilyMemberdictionary = {}
	FamilyIDdictionary = {}
	counter = 1 #keep track of number of families

	with open("540families_idmapping") as f:   # assumes this script is being run from the same directory the mapping file is in
		
		for line in f:
			(key, val) = line.split()
			FamilyMemberdictionary[key] = val #keys are family IDs with extension, values are sample IDs

			familyID = key.split(".")[0]  #removes the extension (.fa, .ma, .p1, .s1)

			if familyID not in FamilyIDdictionary:
				FamilyIDdictionary[familyID] = counter #keys are family IDs without extension
				counter += 1

	#to go through each family ID and write each member's sample ID to a file
	for ID in sorted(FamilyIDdictionary):
		with open (ID +".familyIDs", "w") as famIDs: #create one file for each family
			
			for member, SSC in sorted(FamilyMemberdictionary.items()): #find the SSC# for the father belonging to a particular family
				if member.startswith(ID) and member.endswith("fa"):  
					famIDs.write(SSC + ".recalibrated.haplotypeCalls.vcf.gz" + "\n")

						
			for member, SSC in sorted(FamilyMemberdictionary.items()): 
				if member.startswith(ID) and member.endswith("mo"): #find mother column
					famIDs.write(SSC + ".recalibrated.haplotypeCalls.vcf.gz" + "\n")
				
						
			for member, SSC in sorted(FamilyMemberdictionary.items()): 
				if member.startswith(ID) and member.endswith("s1"):  #find sibling column
					famIDs.write(SSC + ".recalibrated.haplotypeCalls.vcf.gz" + "\n")

						
			for member, SSC in sorted(FamilyMemberdictionary.items()): 
				if member.startswith(ID) and member.endswith("p1"): #find proband column
					famIDs.write(SSC + ".recalibrated.haplotypeCalls.vcf.gz" + "\n")
					

						 

if __name__ == '__main__':
	main()
