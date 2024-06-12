from compare.sketches.sketch import Sketch



class Smallers(Sketch):

    def __init__(self, kmer_streamer=None, size=0, name="Unamed kmer list"):
        # Raise error on null size
        if type(size) is not int or size <= 0:
            raise ValueError("The sketch size must be a positive integer")
        # Initiation of the super-class sketch
        super().__init__(size=size, name=name)

        # --- Complete here if needed ---

        # Init with kmers
        if kmer_streamer is not None:
            self.add_kmers(kmer_streamer)

    def add_kmers(self, kmer_streamer):
        # --- Complete here if needed ---
        raise NotImplmentedError(f"Missing add_kmers method for {type(self)} class")

    def __repr__(self):
        return f"{self.name} {' '.join(str(x) for x in self.kmers)}"
            