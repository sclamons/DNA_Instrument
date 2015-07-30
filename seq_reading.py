from nucleotides import *
from Bio import SeqIO

# Mapping of file endings (i.e., 'fa' in 'a-sequence.fa') to filetypes
# (i.e., 'fasta') for SeqIO.
filetype_map = {'fa'    : 'fasta',
                'fasta' : 'fasta',
                'gb'    : 'genbank'}

def sequences_in_file(filename, mode = 'scaffolds'):
    '''
    Generator returning all of the sequences in a file, as strings. Can handle
    fasta files and genbank files as long as they have a nice standard file
    ending ('.fasta' or '.fa' for fasta, '.gb' for genbank)

    Parameters:
    filename - Name of the file bearing sequences.
    mode     - Either 'scaffolds' or ('ORFs' or 'coding' or 'proteins').
                'scaffolds' -> returns each sequence in the file
                'ORFs' -> returns each coding region it can find as its own
                            sequence.

    Returns: Each of the individual sequences or coding regions in the sequence
                file.
    '''
    filename_ending = filename[filename.rfind('.')+1:]
    seq_filetype    = filetype_map[filename_ending]
    with open(filename, 'rU') as seq_handle:
        for record in SeqIO.parse(seq_handle, seq_filetype):
            if mode == 'scaffolds':
                yield str_to_nucleotide(str(record.seq))
            elif mode in ['ORFs', 'coding', 'proteins']:
                counter = 0
                for coding_region in coding_regions_in(str(record.seq)):
                    counter += 1
                    #print("Parsing coding sequence #" + str(counter))
                    yield coding_region#str_to_nucleotide(coding_region)
            else:
                raise Exception('Invalid sequence file read mode "' + mode +
                                '"')

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

def coding_regions_in(sequence):
    '''
    Find the coding regions in a sequence. Returns them in the order they first
    appear in the genome, regardless of orientation
    '''
    forward_start, forward_end = find_next_forward_indexes(sequence, 0)
    #print("First forward found from " + str(forward_start) + " to " + str(forward_end))
    rev_start, rev_end         = find_next_reverse_indexes(sequence, 0)
    #print("First reverse found from " + str(rev_end) + " to " + str(rev_start))
    while forward_start or rev_start:
        if not rev_start or (forward_start and forward_start <= rev_end):
            yield sequence[forward_start:forward_end]
            forward_start, forward_end = \
                                find_next_forward_indexes(sequence, forward_end)
            #print("Next forward found from " + str(forward_start) + " to " + str(forward_end))
        else:
            yield reverse_complement(sequence[rev_end:rev_start])
            rev_start, rev_end = find_next_reverse_indexes(sequence, rev_start)
            #print("Next reverse found from " + str(rev_end) + " to " + str(rev_start))

def find_next_forward_indexes(sequence, start_pos):
    next_forward_start = sequence.find(START, start_pos)
    next_forward_stop  = None
    for pos in range(next_forward_start, len(sequence), 3):
    #    print("Checking F: " + str(sequence[pos:pos+3]))
        if sequence[pos:pos+3] in STOPS:
            next_forward_stop = pos + 3
            break
    if not next_forward_stop:
        next_forward_stop = len(sequence)
    return next_forward_start, next_forward_stop

def find_next_reverse_indexes(sequence, start_pos):
    next_rev_start = 3 + sequence.find(reverse_complement(START), start_pos)
    x = 0
    while True:
        x += 1
        #print("Try #" + str(x) + ", next_rev_start = " + str(next_rev_start))
        #print(range(next_rev_start, start_pos-1, -3))
        #print("start_pos = " + str(start_pos))
        if next_rev_start == 2:
        #    print("Out of sequence")
            return None, None
        next_rev_end = None
        for pos in range(next_rev_start, start_pos-1, -3):
        #    print("Checking R: " + str(pos-3) + ", " + str(pos))
            if reverse_complement(sequence[pos-3:pos]) in STOPS:
                next_rev_end = pos - 3
                break
        if next_rev_end:
            return next_rev_start, next_rev_end
        else:
        #    print("No end found")
            next_rev_start = \
                3 + sequence.find(reverse_complement(START), next_rev_start+1)

