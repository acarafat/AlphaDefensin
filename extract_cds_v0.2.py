# Extract CDS v 0.2

# Project: Alpha Defensin Evolutionary Analysis
# Date: 5 February 2015
# Author: ARF

# This script takes a nucleotide sequence as input along with 'join' information
# of CDS from genebank format of NCBI. Then it returns user a intron deleted CDS
# sequence.




import sys

print 'Please enter sequence here and press CONTROL+D to finish: \n'

s = sys.stdin.readlines()
join = raw_input('Please enter the "join" info and press ENTER: ')

seq = ''.join(s).replace('\n', '')

cdsN = ''

for i in join.split(','):
    index = i.split('..')
    cdsN += seq[int(index[0])-1: int(index[1])]

print cdsN
print len(cdsN)%3.0


