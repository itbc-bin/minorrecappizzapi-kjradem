def check_dna(function):
    def wrapper(sequence):
        for letter in sequence.lower():
            if letter not in ['a', 't', 'c', 'g']:
                print('This is an invalid sequence')
                return
        function(sequence)
    return wrapper


@check_dna
def dna_to_rna(sequence):
    return sequence.upper().replace('T', 'U')


rna_seq = dna_to_rna("ACGT")
# TO-DO: rna_seq returns NoneType, should be str
print(rna_seq)