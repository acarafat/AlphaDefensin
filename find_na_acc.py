# NA Accession finder

# Alpha Defensin Project
# For Mining PSI BLAST Output

# Arafat Rahman
# 25 April 2016

# What it does:
# Inspect gb entry. 
# Go to xref for gene database if present.
# Extract NA accession number 
# Extract NA sequence using join information in genbank file

# Import Modules
#from Bio import SeqIO
#from Bio import Entrez
import urllib2
from time import sleep

# Import Datasets
from find_na_acc_dump import geneID, links

# Remove duplicates in links
unique_links = list(set(links))
unique_links.remove('')

# Define e-mail for Entrez search using Biopython
#Entrez.email = 'arafat@nstu.edu.bd'


def extract_geneID(handle):
    '''
    Objective: Extract db_xref qualifier from CDS feature of a GenBank entry 
    only if it contain GeneID key. 
    Input: A file containing GenBank sequences
    Output: A list containing entry of db_xref that refers to NCBI Gene database
    '''    
    db_xref = []
    for record in SeqIO.parse(handle, 'genbank'):
        for feature in record.features:
            if feature.type == 'CDS':
                try:
                    if 'GeneID' in ''.join(feature.qualifiers['db_xref']):
                        GeneID = [int(i.split(':')[1]) for i in feature.qualifiers['db_xref'] if 'GeneID' in i][0]
                        #db_xref.append(feature.qualifiers['db_xref'])
                        db_xref.append(GeneID)
                except:
                    pass
    return db_xref

def extract_NA_acc(GeneID):
    '''
    Objective: Extract accession number of nucleotide sequence 
    from a single gene id
    Input: A GeneID
    Output: A Nucleotide Accession Number
    '''
    url = 'http://www.ncbi.nlm.nih.gov/gene/?term=' + str(GeneID)
    response = urllib2.urlopen(url)
    html = response.read()
    start = html.find('Go to nucleotide:</strong>')
    end = html.find('GenBank</a>', start)
    target = html[start:end].split('href=')[-1].split('ref')[0]
    return target.strip().replace('"','')
    
def extract_NA_sequence(link):
    '''
    Objective: Extract CDS from genbank file using its join info.
    Input: Link to genbank file
    Output: CDS
    '''
    acc = link.split('/')[2].split('?')[0]
    start_pos = int(link.split('=')[-2].split('&amp')[0])
    try:
        stop_pos = int(link.split('=')[-1])
    except:
        stop_pos = int(links[1].split(';')[-2].split('=')[-1].split('&')[0])
    try:
        handle = Entrez.efetch(db='nucleotide', rettype = 'gb', retmode = 'text',
                               seq_start = start_pos, seq_stop = stop_pos, id = acc)
        record = SeqIO.read(handle, 'genbank')
        for feature in record.features:
            if feature.type =='CDS':
                join = feature.location
                cds = join.extract(record.seq)
                return record.id, record.description, cds
    except:
        print acc, 'not found!'
    
     


if __name__ == '__main__':
    #handle = '../Dataset/psi_blast_NP_001289194.1.gb'
    #db_xref = extract_geneID(handle)
    #url_target = []
    #count = 1
    #for i in geneID:
    #    print 'Progress: ', count, '/', len(geneID)
    #    count += 1
    #    url_target.append(extract_NA_acc(i))
    #print ''
    #print url_target

    #cds_sequences = []
    #count = 1
    #for entry in unique_links:
    #    print 'Progress: ', count, '/', len(links)
    #    output = extract_NA_sequence(entry)
    #    cds_sequences.append(output)
    #    count += 1
    #    if count%3 == 0:
    #        sleep(3)
    pass
