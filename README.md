
# First steps - Understand the code

For this practical session everything that is not directly related to the sketches is already coded.
This repository code contains all the primitive to enumerate kmers from fasta files, to select one type of sketch for comparison and to compare sequences using Jaccard index.
You work during this session will be to complete the code of the different types of sketches.
Each sketch type is a class in Python that is present in the `compare.sketches` module.
A fake sketch (file all_kmers.py) that keeps all the kmers to compute the Jaccard index is already coded.
All the other classes in the `compare.sketches` module will be completed along this practical session.

In the following sections you find some fasta files to test the sketches comparison on them.
Viruses can be used for small tests. All the sketches should easily scale on bacteria but depending on your implementation some of them could struggle on the large eukaryote files.

## Datasets

Viruses:

* https://www.ncbi.nlm.nih.gov/nuccore/NC_045512.2?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/NC_006577.2?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/MZ009823.1?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/OM371884.1?report=fasta

Bacteria:

Eukaryotes:


The following command lines can be used for comparison.
For the first test you can use `--sketch-type all` on viruses, this will compute the Jaccard index using all the kmers from the sequences.

## Command lines

From the root directory of the project:
* Comparison of 2 genomes
```bash
    python3 -m compare --comparison-mode pair -k <kmer_size> --sketch-type <sketch_type:{all,smin,buckets,hyper}> <file1.fasta> <file2.fasta>
```
* All vs all genomes
```bash
    python3 -m compare --comparison-mode set -k <kmer_size> --sketch-type <sketch_type:{all,smin,buckets,hyper}> <directory>
```


## Code inspection

Let's open the code.
The main that is called for our session is in the compare module and is called `__main__.py` (this naming is mandatory to trigger the module loading on `python3 -m` command).
The important code is after the comment with dashed lines.
The first step load the selected sketch for each file that will be compared.
Then pair by pair the sketches are computing the Jaccard index.

If you open the KmerStreamer class (in compare/utils/kmers.py) you can notice the usage of the keyword yield in the stream method.
This allow the streaming of the kmers in a for loop without holding all of them at the same time in memory.

In the AllKmer fake sketch the "algorithm" is implemented in the `add_kmers` function.
This is this function that you will implement in the other sketch classes.
You can also notice that the Jaccard computation function is not present here but in the mother class Sketch as it will always be the same function.
This Jaccard function rely on the fact that the sketches are holding their kmers in a frozenset.
So, whatever your implementation are, at the end, all the sketch kmers must be in a frozenset in the `self.kmers` property of the sketch object.


## First step - Adding the hash function

As you can see in the kmer streaming function, there is no hashing of the value.
So, right now, this is the alphabetic encoding that is returned by the streamer.

Questions:
* Can you use the xorshift64 function present in `compare/utils/xorshift.py` to hash the kmer in the streamer ?
* Can you modify the streamer constructor in such a way that the flag `--xorshift` of the command line activate the hashing ? (without the flag the current behavior should remain).


