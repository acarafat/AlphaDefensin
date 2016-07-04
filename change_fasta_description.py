# Update Fasta Description

# Arafat
# 20 April 2016

from Bio import SeqIO


#target fasta file to change description
target_file = '../Dataset/new_genomes/zika-genomeapril-june_no-5-utr.fas' 

#preporcess csv file containing sequence meta-information
raw = open('../Dataset/new_genomes/zika_genome_new-25.csv').read().split('\n')
raw.remove('')

meta_info = {i.split(',')[0].strip():i.split(',') for i in raw}

# Initiate list to store updated sequence record 
store = []

# Update sequence record
for seq_record in SeqIO.parse(target_file, 'fasta'):
    gb_acc = seq_record.id.split('|')[-2].strip()
    if gb_acc in meta_info.keys():
        seq_record.id = ''
        seq_record.description = gb_acc+'_'+'_'.join(meta_info[gb_acc]).strip()
        store.append(seq_record)


# Write updated sequence records in a file
SeqIO.write(store, '../Dataset/new_genomes/25genome_updated.fasta', 'fasta')        
