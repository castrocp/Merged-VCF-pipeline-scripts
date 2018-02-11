#!/bin/bash

# This script can be used to filter down the full list of candidate de novo variants to the ones that only appear a certain number of times.  At the time of writing this, for example, I only want the variants that do not appear more than twice.  

# Combine the chromosome column and start coordinate column with an underscore so that I can differentiate between identical coordinates on different chromosomes
awk '{print $1"_"$2}' AllCandidateDenovos.bed | 

# will create a new column that tells how many times each chrom/start combination appears
uniq -c | 

# print the chrom/start coordinates that appear at most twice
awk '$1 <= 2 {print $2}' |

# subsitute underscores with tabs, to recover the original column format
sed 's/_/\t/g' > DenovosTwiceOrLess.txt

# pull lines from the original de novo variant file containing only coordinates in the file that was just created (returning variants that only appear twice, at most.
grep -Ff DenovosTwiceOrLess.txt AllCandidateDenovos.bed > DenovosAppearingTwiceOrLess.bed
