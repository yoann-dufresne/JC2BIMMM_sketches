from abc import ABC, abstractmethod


class Sketch(ABC):

    def __init__(self, size=0, name="Unamed kmer list"):
        self.name = name
        self.size = size
        self.kmers = frozenset([])

    @abstractmethod
    def add_kmers(self, kmer_streamer):
        pass

    def save(self, filename):
        with open(filename, 'w') as fp:
            for kmer in self.kmers:
                print(str(kmer), file=fp)

    def load(self, filename):
        kmer_list = []
        with open(filename) as fp:
            for line in fp:
                if len(line) > 0:
                    kmer_list.append(int(line))

        self.kmers = frozenset(kmer_list)

    def jaccard(self, other):
        intersection_size = len(self.kmers & other.kmers)
        union_size = len(self.kmers) + len(other.kmers) - intersection_size
        return intersection_size / union_size
            