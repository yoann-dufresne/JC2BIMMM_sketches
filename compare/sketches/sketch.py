from abc import ABC, abstractmethod


class Sketch(ABC):

    def __init__(self, name="Unamed kmer list"):
        self.name = name
        self.kmers = frozenset([])

    @abstractmethod
    def add_kmers(self, kmer_streamer):
        pass

    def jaccard(self, other):
        intersection_size = len(self.kmers & other.kmers)
        union_size = len(self.kmers) + len(other.kmers) - intersection_size
        return intersection_size / union_size
            