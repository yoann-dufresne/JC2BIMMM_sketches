from compare.sketches.sketch import Sketch



class Partitions(Sketch):

    def __init__(self, kmer_streamer=None, size=0, name="Unamed kmer list"):
        # Raise error on null size
        if type(size) is not int or size <= 0:
            raise ValueError("The sketch size must be a positive integer")
        # Initiation of the super-class sketch
        super().__init__(size=size, name=name)

        self.kmers = [18446744073709551615 for _ in range(self.size)]

        # Init with kmers
        if kmer_streamer is not None:
            self.add_kmers(kmer_streamer)

    def add_kmers(self, kmer_streamer):
        for kmer in kmer_streamer.stream():
            # Compute the partition index
            partition_idx = kmer % len(self.kmers)
            # Compare with previous value
            if kmer < self.kmers[partition_idx]:
                # Remove the largest kmer in the sketch
                self.kmers[partition_idx] = kmer

        self.kmers = frozenset(self.kmers)

    def __repr__(self):
        return f"{self.name} {' '.join(str(x) for x in self.kmers)}"
            