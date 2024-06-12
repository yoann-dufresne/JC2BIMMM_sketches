from compare.sketches.sketch import Sketch



class HyperMin(Sketch):

    def __init__(self, kmer_streamer=None, name="Unamed kmer list"):
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
            