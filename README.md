
# Command lines

From the root directory of the project:
* Comparison of 2 genomes
```bash
    python3 -m compare --mode pair <file1.fasta> <file2.fasta> data/ -k 15
```
* All vs all genomes
```bash
    python3 -m compare --mode all <directory> -k 15
```

# Datasets

Viruses:

* https://www.ncbi.nlm.nih.gov/nuccore/NC_045512.2?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/NC_006577.2?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/MZ009823.1?report=fasta
* https://www.ncbi.nlm.nih.gov/nuccore/OM371884.1?report=fasta

Bacterias:

Eukariotes: