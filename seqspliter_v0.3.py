# Split Sequence
# Project: Alpha Defensin
# Task: Split def domain encoding region from propeptide.

# Arafat
# 27 February 2016


from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def file_input(filename, header= False):
    '''
    csv file in and pre processing
    Input: a csv which do not have table-header. If header present, 
    header = True should be used.
    Output: a list containing sequence id and index for splitting
    '''
    readcsv = open(filename, 'r').read()
    if header == True:
        csv_data = readcsv.split('\n')[1:]
    else:
        csv_data = readcsv.split('\n')
    if '' in csv_data:
        csv_data.remove('')
    return csv_data


def get_index(csv_data):
    '''
    Split csv_data entry on ',' and then store given index position
    Input: start and stop position 
    Output: a dictionary whose key is sequence id/description and value is 
    start and stop position
    '''
    # indices info from csv file
    indices =  [[i.split(',')[0],i.split(',')[1], i.split(',')[2], 
                i.split(',')[3], i.split(',')[4]] for i in csv_data]
    return indices


def original_sequences(seq_file):
    '''
    Load sequence in a dictionary for splitting
    '''
    seq_record = [[i.description, i.seq] for i in SeqIO.parse(seq_file, 'fasta')]
    return seq_record

def split_sequences(indices, seq, start, end):
    # splitting sequence 
    # The problem is here
    splitted_seq = []
    count = 0
    for i in indices.keys():
        seq_id =  '_'.join(i.split('_')[0:2])[1:]
        for d in seq.keys():
            if seq_id in d:
                count += 1
                try:
                    sub_seq = SeqRecord(seq[d][int(indices[i][start])*3:int(indices[i][end])*3+4], id = seq_id, description = d)
                    splitted_seq.append(sub_seq)
                except:
                    pass
                break
    return splitted_seq
    
          
if __name__ == '__main__':
    csv_data = file_input('../Dataset/SMART-Analysis-Information-All.csv', True)
    indices = get_index(csv_data)
    seq = original_sequences('../Dataset/def_seqs_CDS.fas')
    #splitted_seq = split_sequences(indices, seq, 0, 3)
    #SeqIO.write(splitted_seq, '../Dataset/propeptides.fas', 'fasta')                


