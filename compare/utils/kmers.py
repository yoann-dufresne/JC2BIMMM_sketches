from compare.utils.loading import load_fasta
from compare.utils.xorshift import xorshift64

class KmerStreamer:
    def __init__(self, filename, k, hash=False):
        self.filename = filename
        self.k = k
        self.hash = hash

    def stream(self):
        for sequence in load_fasta(self.filename):
            for kmer in self.stream_from_seq(sequence):
                yield kmer

    def stream_from_seq(self, sequence):
        # Precompute the (k-1)-mer (and reverse)
        k = self.k
        kmer = 0
        rkmer = 0
        seq_idx = 0
        used_nucl = 0
        while used_nucl < k-1:
            letter = sequence[seq_idx]
            seq_idx += 1
            if letter == 'N':
                continue
            used_nucl += 1

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
        for seq_idx in range(used_nucl, len(sequence)):
            letter = sequence[seq_idx]
            if letter == 'N':
                continue

            # Forward kmer
            kmer <<= 2
            letter_value = (ord(letter) >> 1) & 0b11
            kmer += letter_value
            kmer &= mask
            # Reverse kmer
            rkmer >>= 2
            rev_letter_value = (letter_value + 2) & 0b11
            rkmer += rev_letter_value << (2 * (k - 1))

            yield min(xorshift64(kmer), xorshift64(rkmer))