from nucleotides import *
from Bio import SeqIO

# Mapping of file endings (i.e., 'fa' in 'a-sequence.fa') to filetypes
# (i.e., 'fasta') for SeqIO.
filetype_map = {'fa'    : 'fasta',
                'fasta' : 'fasta',
                'gb'    : 'genbank'}

def sequences_in_file(filename):
    '''
    Generator returning all of the sequences in a file, as strings. Can handle
    fasta files and genbank files as long as they have a nice standard file
    ending ('.fasta' or '.fa' for fasta, '.gb' for genbank)

    '''
    filename_ending = filename[filename.rfind('.')+1:]
    seq_filetype    = filetype_map[filename_ending]

    with open(filename, 'rU') as seq_handle:
        for record in SeqIO.parse(seq_handle, seq_filetype):
            yield str_to_nucleotide(str(record.seq))

def str_to_nucleotide(seq_str):
    '''
    Generator for converting a string representing a sequence into nucleotide
    values.
    '''
    for n in seq_str:
        if   n.upper() == 'A':
            yield A
        elif n.upper() == 'T':
            yield T
        elif n.upper() == 'C':
            yield C
        elif n.upper() == 'G':
            yield G
        else:
            yield N