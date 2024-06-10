from compare.sketches.sketch import Sketch



class AllKmers(Sketch):

    def __init__(self, kmer_streamer=None, name="Unamed kmer list"):
        # Initiation of the super-class sketch
        super().__init__(name)
        # Init with kmers
        if kmer_streamer is not None:
            self.add_kmers(kmer_streamer)

    def add_kmers(self, kmer_streamer):
        kmers = []

        # Append the kmers one by one to a temporary kmer vector
        for kmer in kmer_streamer.stream():
            # select the minimal kmer between forward and reverse
            kmers.append(kmer)

        # Group sequences kmers with the previous kmers. The frozenset remove duplicates and allow unions over sets.
        #          v This is a union operation
        self.kmers |= frozenset(kmers)

    def __repr__(self):
        return f"{self.name} {' '.join(str(x) for x in self.kmers)}"
            