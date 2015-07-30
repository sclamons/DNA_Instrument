A = 0
T = 1
C = 2
G = 3
N = 4

START = 'ATG'
STOPS = ['TAG', 'TAA', 'TGA']
COMPLEMENTS = {'G' : 'C',
               'C' : 'G',
               'A' : 'T',
               'T' : 'A',
               G   : C,
               C   : G,
               A   : T,
               T   : A}

def reverse_complement(seq):
    return_seq = ""
    for i in range(len(seq)-1, -1, -1):
        return_seq += COMPLEMENTS[seq[i]]
    return return_seq


