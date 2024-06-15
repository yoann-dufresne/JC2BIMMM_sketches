from compare.sketches.sketch import Sketch




class HyperMin(Sketch):

    def __init__(self, kmer_streamer=None, size=0, name="Unamed kmer list"):
        # Initiation of the super-class sketch
        super().__init__(size=size, name=name)

        self.kmers = array('H', [65535 for _ in self.size])

        # Init with kmers
        if kmer_streamer is not None:
            self.add_kmers(kmer_streamer)

    def load(self, filename):
        self.kmers = array('H', [65535 for _ in self.size])
        with open(filename) as fp:
            for idx, line in enumerate(fp):
                if len(line) == 0:
                    continue
                val = int(line.strip())
                self.kmers[idx] = val

    def add_kmers(self, kmer_streamer):
        # --- Complete here if needed ---
        raise NotImplmentedError(f"Missing add_kmers method for {type(self)} class")

    def __repr__(self):
        return f"{self.name} {' '.join(str(x) for x in self.kmers)}"
            