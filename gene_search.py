# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 10:50:36 2016

@author: arafat
"""
import urllib2
from Bio import Entrez


# This is an output of data mining using readTSVFile'gene list.tsv file')
info =  {1667: ['NC_000008.11', '6977649', '6980122', 'minus'],
 105881500: ['NW_012197698.1', '11850', '14308', 'minus']}
    
def fetchSource(gene_id):
    ''' This function can be used for obtaining nucleotide database accession, 
    from & to base positions and strand of a given gene id in gene database.
    
    This function fetch source html of given id and find the fasta link information.
    
    Only use when there is not enough information in the input file of 
    database record.
    '''
    url = 'http://www.ncbi.nlm.nih.gov/gene/?term=' + str(gene_id)
    response = urllib2.urlopen(url)
    html = response.read()
    posInit = html.find("\"Nucleotide FASTA report\"")
    posFinal = html.find("ref", posInit+31)
    return html[posInit:posFinal]
    
def readSummaryFile(fileName):
    '''
    !!!Not developed!!!
    '''
    rawData = open(fileName).read().split('\n\n')
    for data in rawData:
        dataList = data.split('\n')
        if '' in dataList == True:
            dataList.remove('')
    pass

def readTSVfile(fileName):
    '''
    Extract necessary information. Returns a dictionary.
    {gene_id: [nt_accession, start_pos, end_pos, strand]}
    
    if first two information not present about a field, need to use
    fetchSource function to collect it from NCBI.
    '''
    rawData = open(fileName).read().split('\n')
    info = {}
    notFound = []
    for record in rawData[1:]:
        if record.split('\t')[-6] != '' or record.split('\t')[-5] != '':
            info[int(record.split('\t')[2])] = [record.split('\t')[11], record.split('\t')[-6], record.split('\t')[-5], record.split('\t')[-4]]
        else:
            raw = fetchSource(int(record.split('\t')[2]))
            try:
                accession = raw.split('core/')[1].split('?')[0]
                nt_start = raw[raw.find('from=')+5 : raw.find('&amp', raw.find('from='))]
                if 'strand=true' in raw:
                    nt_end = raw[raw.find('to=')+3 : raw.find('&', raw.find('to='))]
                    nt_strand = 'minus'
                else:
                    nt_end = raw[raw.find('to=')+3 : ]
                    nt_strand = 'plus'
                info[int(record.split('\t')[2])] = [accession, nt_start, nt_end, nt_strand]
            except:
                notFound.append(int(record.split('\t')[2]))
                continue
    return info
            
    
# Fetch sequece using Entrez
def mineEntrez(paramInfo):
    '''
    Mine NCBI nucleotide database for defined sequence
    '''
    Entrez.email = 'arafat@nstu.edu.bd'
    seq = ''
    for k in paramInfo.keys():
        accID = paramInfo[k][0]
        begin = paramInfo[k][1]
        end = paramInfo[k][2]
        if paramInfo[k][3] == 'plus':
            s = 1
        else:
            s = 2
        if '"' in end:
            end = end[:end.find('"')]
        handle = Entrez.efetch(db = 'nucleotide', id = str(accID),
                               rettype = 'fasta', retmode = 'text', strand = s, 
                               seq_start = int(begin), seq_stop = int(end))
        seq += handle.read()
    return seq
    

    
if __name__ == '__main__':
    readFile('alpha defensin gene database.txt')
    
            
