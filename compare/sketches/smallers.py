from compare.sketches.sketch import Sketch



class Smallers(Sketch):

    def __init__(self, kmer_streamer=None, size=0, name="Unamed kmer list"):
        # Raise error on null size
        if type(size) is not int or size <= 0:
            raise ValueError("The sketch size must be a positive integer")
        # Initiation of the super-class sketch
        super().__init__(size=size, name=name)

        self.kmers = [18446744073709551615 for _ in range(self.size)]
        self.max = 18446744073709551615

        # Init with kmers
        if kmer_streamer is not None:
            self.add_kmers(kmer_streamer)

    def add_kmers(self, kmer_streamer):
        for kmer in kmer_streamer.stream():
            if kmer < self.max:
                # Remove the largest kmer in the sketch
                self.kmers.remove(max(self.kmers))
                # Add the new kmer
                self.kmers.append(kmer)
                # Recompute the max from the sketch
                self.max = max(self.kmers)

        self.kmers = frozenset(self.kmers)

    def __repr__(self):
        return f"{self.name} {' '.join(str(x) for x in self.kmers)}"
            