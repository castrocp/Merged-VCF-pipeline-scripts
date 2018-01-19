#!/bin/bash

#Run this command as mergeVCF.sh from the directory the *.familyIDs files are in

for file in *.familyIDs;
	do
	cat $file | while read line;
		do
		find /home/castrocp/../../data/SSC2/efs/ -name "$line";
		done| xargs vcf-merge | gzip > ${file}.merged.vcf.gz;
	done
done


