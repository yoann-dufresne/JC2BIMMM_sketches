
# First steps - Understanding the code
<details>
<summary>-- first steps</summary>

For this practical session everything that is not directly related to the sketches is already coded.
This repository code contains all the primitive to enumerate kmers from fasta files, to select one type of sketch for comparison and to compare sequences using Jaccard index.
Your work during this session will be to complete the code of the different types of sketches.
Each sketch type is a class in Python that is present in the `compare.sketches` module.
A fake sketch (file `all_kmers.py`) that keeps all the kmers to compute the Jaccard index is already coded.
All the other classes in the `compare.sketches` module will be completed along this practical session.

In the following sections you will find some fasta files to test the sketches comparison on them.
Viruses can be used for small tests. All the sketches should easily scale on bacteria but depending on your implementation some of them could struggle on large eukaryote files.

## Datasets

Viruses:

* https://www.ncbi.nlm.nih.gov/nuccore/NC_045512.2?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/NC_006577.2?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/MZ009823.1?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/OM371884.1?report=fasta

Bacteria:

* https://www.ncbi.nlm.nih.gov/nuccore/NZ_CP050202.1?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/NZ_CP050205.1?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/NZ_CP050201.1?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/NZ_CP050214.1?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/NZ_CP050218.1?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/NZ_CP050208.1?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/NZ_CP050211.1?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/NZ_VCKP01000001.1?report=fasta

Eukaryotes:

* https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/002/985/GCF_000002985.6_WBcel235/GCF_000002985.6_WBcel235_genomic.fna.gz
* https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_genomic.fna.gz
* https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/010/183/535/GCF_010183535.1_CRPX506/GCF_010183535.1_CRPX506_genomic.fna.gz


The following command lines can be used for comparison.
For the first test you can use `--sketch-type all` on viruses. This will compute the Jaccard index using all the kmers from the sequences.

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
The first step loads the selected sketch for each file that will be compared.
Then pair by pair the sketches are computing the Jaccard index.

If you open the KmerStreamer class (in `compare/utils/kmers.py`) you can notice the usage of the keyword yield in the stream method.
This allows the streaming of the kmers in a for loop without holding all of them at the same time in memory.

In the AllKmer fake sketch the "algorithm" is implemented in the `add_kmers` function.
This is this function that you will implement in the other sketch classes.
You can also notice that the Jaccard computation function is not present here but in the mother class Sketch as it will always be the same function.
This Jaccard function relies on the fact that the sketches are holding their kmers in a frozenset.
So, whatever your implementation is, at the end, all the sketch kmers must be in a frozenset in the `self.kmers` property of the sketch object.


## First step - Adding the hash function

As you can see in the kmer streaming function, there is no hashing of the value.
So, right now, this is the alphabetic encoding that is returned by the streamer.

Exercises:
* Can you use the `xorshift64` function present in `compare/utils/xorshift.py` to hash the kmer in the streamer ?
* Can you modify the streamer constructor in such a way that the flag `--xorshift` of the command line activates the hashing ? (without the flag, the current behavior should remain).

## Comparing the implementations

It exists many ways of measuring the time/memory usage for a given piece of software.
Here we will focus on simple metrics that are global time and global memory.
By using the `/usr/bin/time -v` as prefix of your command, you will be able to measure the "Elapsed time" and the "Maximum resident set size" which are respectively time and memory that you want to measure.

Exercise:
* Compare the time and memory usages on the same pair of fasta activating/deactivating the hash function.

</details>

# Bottom-s MinHash

<details>
<summary>-- bottom-s MinHash</summary>

In the bottom-s sketch we only want to keep *s* kmers.
One strategy could be to load all kmers, sort the list and only keep the *s* first kmers of that list.
However, the list costs in memory *k* times the size of the input sequence.
So it rapidly becomes impractical to load all the kmers.
Here we want to only keep *s* kmers in memory at a time.

## First strategy - remember the max of the bottom

The strategy can be: For each new kmer visited during the enumeration, compare it with the largest kmer stored in the sketch.
If it is smaller than the maximum value of the sketch, then remove the max and replace it by the current kmer.

Exercises:
* Implement the add_kmers of the `Smallers` sketch class.
* On small datasets, compare the real Jaccard index with the approximate Jaccard given by this sketch implementation. What is the influence of the sketch size ?
* Does the xorshift activation/deactivation change the results ?

<details>
<summary>(optional) Intermediate difficulty exercises</summary>

* What is the complexity of the strategy (regarding *s*, the size of the sketch, *k*, the size of the kmers and *n* the size of the sequence) ?

</details>


<details>
<summary>(optional) Intermediate difficulty - second implementation using heapq</summary>

## Second strategy - order the bottom values

Looking for max value can be expensive on large sketches.
We would like to store the kmers in such a way that the largest element is always known, it can be extracted in constant time and new elements can be inserted very quickly.
The Heap Queue is a datastructure that has exactly these properties and the heapq library from python already implement everything we need for improving our sketch.

Exercises:
* Use the heapq python library to speedup the creation of the bottom-s sketch.
* Compare the exec time with the previous implementation.
* Did the Jaccard index estimation change and why ?

</details>

</details>

# Partition MinHash

<details>
<summary>-- Partition MinHash</summary>

In this section we will implement the *partition MinHash* sketch.
The idea behind it is to make the *s* values from the sketch independent from each other such as no ordering is needed for sketch comparison.
So, a *p-sketch* (partition sketch), is composed of *s* partitions.
When we compute the hash value of a kmer, we then want to always assign it to the same partition.
For that, we can use the modulus operation.

So, a full computation for a kmer contains these steps:
* Compute the hash of a kmer
* Get the partition index for that value
* Compare the kmer present in that partition with the current kmer and only keep the smallest.

Exercises:
* Implement the partition sketch
* Is it faster or slower than the previous sketch comparison ? Is there a memory difference ?
* Is it closer than the previous sketch from the real Jaccard value ?

<details>
<summary>(optional) Intermediate difficulty exercises</summary>

* What is the complexity of the strategy (regarding *s*, the size of the sketch, *k*, the size of the kmers and *n* the size of the sequence) ?

</details>


</details>


<details>
<summary>(Optional) For advanced programmers</summary>

# HyperMinHash

<details>
<summary>-- HyperMinHash</summary>

In the different sketches we select a certain number of hash values because they are smaller than others.
This selection process have a direct consequence: the binary representation of the integers have a lot of leading 0s.
It means that the information is mostly contained in the lower part of the integer and the leading bits are mostly useless.
So, we can change the way we represent the 64-bits integer of our hash to take advantage of that property.
As described in the course, we can encode the position of the first 1 in the integer and complete with some lower bits of the original integer (cf figure).
For large sets of kmers, we can expect to encode the 64 bits hash values in 16 bits integer with a limited loss of information along the compression.

![alt text](https://github.com/yoann-dufresne/JC2BIMMM_sketches/blob/main/HyperMin.png?raw=true)

Python is a language where the integer have arbitrary large integer values.
All the encoding is completely hidden under the hood of the language.
To be able to create list of controlled size integer we need to use libraries.
For lists of 16 bits integer we can use the array module with "unsigned short" integers: https://docs.python.org/3/library/array.html

Exercises:
* Implement the `add_kmers` of the Hypermin sketch class.
* The set operations are not defined on the datastructure. Redefine the `jaccard` function in the class to fit with the array representation of the sketch.
* How the results change on a sketch with the same number of hash value than the partition sketch ?
* Same question but with the same memory usage ?

* __Super-Bonus__: How can we take advantage of the partitionning technics to save even more space ? Hint: Ask Victor Levallois about his last paper :)


</details>
</details>
