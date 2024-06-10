from compare.utils.loading import load_fasta


class KmerStreamer:
    def __init__(self, filename, k):
        self.filename = filename
        self.k = k

    def stream(self):
        for sequence in load_fasta(self.filename):
            for kmer in self.stream_from_seq(sequence):
                yield kmer

    def stream_from_seq(self, sequence):
        # Precompute the (k-1)-mer (and reverse)
        k = self.k
        kmer = 0
        rkmer = 0
        for letter in sequence[:k-1]:
            # A = 00, C = 01, T = 10, G = 11
            # Forward kmer
            kmer <<= 2
            letter_value = (ord(letter) >> 1) & 0b11
            kmer += letter_value
            # Reverse kmer
            rkmer >>= 2
            rev_letter_value = (letter_value + 2) & 0b11
            rkmer += rev_letter_value << (2 * (k - 1))

        # Stream kmers
        mask = (1 << (2 * k)) - 1
        for letter in sequence[k-1:]:
            # Forward kmer
            kmer <<= 2
            letter_value = (ord(letter) >> 1) & 0b11
            kmer += letter_value
            kmer &= mask
            # Reverse kmer
            rkmer >>= 2
            rev_letter_value = (letter_value + 2) & 0b11
            rkmer += rev_letter_value << (2 * (k - 1))

            yield min(kmer, rkmer)