import argparse
from sys import stderr, argv
from os import path, listdir
from itertools import combinations

from compare.utils.kmers import KmerStreamer
from compare.sketches.all_kmers import AllKmers
from compare.sketches.smallers import Smallers
from compare.sketches.buckets import Buckets
from compare.sketches.hypermin import HyperMin


def parse_cmd():
    print("Command line called:")
    print(f"{' '.join(argv)}")
    print()

    # Setup the command line
    parser = argparse.ArgumentParser(
        prog="sketch tester",
        description="the program is to test the efficiency of different sketches"
    )

    parser.add_argument('-k', type=int, required=True, help="kmer size.")
    parser.add_argument('-c', "--comparison-mode", choices=['pair', 'set'], default='pair', help="Exec mode can be 'pair' of 'set'. In 'pair' mode the software will compare 2 genomes in files pointed by the 2 positionnal argument of the command. In 'set' mode, all the genomes in a directory will be compared using sketches. The directory path must be the first positional argument. Default value is 'pair'.")
    parser.add_argument('-t', '--sketch-type', choices=['all', 'smin', 'buckets', 'hyper'], default='all', help="Type of sketch to use for the comparison(s).")
    parser.add_argument('-x', '--xorshift', action='store_true', help="Activated the xorshift function to hash kmers.")
    parser.add_argument('-s', '--size', type=int, default=1024, help="Sketch size.")
    parser.add_argument('paths', nargs='+', help="path(s) to data. See mode for more details.")

    # Parse arguments of the command line
    args = parser.parse_args()

    # args verification
    if args.comparison_mode == 'pair' and len(args.paths) < 2:
        print("'pair' mode needs 2 files as arguments", file=stderr)
        parser.print_help()
        exit(1)

    return args



if __name__ == "__main__":
    args = parse_cmd()

    files_to_load = []

    # Pair mode that compare 2 files:
    if args.comparison_mode == 'pair':
        # Verify file presence
        fa1, fa2 = args.paths[0:2]
        if not path.isfile(fa1):
            print(f"Absent file {fa1}", file=stderr)
            exit(2)
        if not path.isfile(fa2):
            print(f"Absent file {fa2}", file=stderr)
            exit(2)
        files_to_load.append(fa1)
        files_to_load.append(fa2)

    # All vs all in a directory
    else:
        # Verify directory presence
        dirpath = args.paths[0]
        if not path.isdir(dirpath):
            print(f"Path {dirpath} should be a valid directory containing all the sequences to compare")
            exit(2)

        # Load fasta names
        fasta_extensions = ["fasta", "fa", "fna"]
        for filename in listdir(dirpath):
            extension = filename[filename.rfind('.')+1:]
            if extension in fasta_extensions:
                files_to_load.append(path.join(dirpath, filename))

    # Select the sketch type
    sketch_types = {
        'all' : AllKmers,
        'smin' : Smallers,
        'buckets' : Buckets,
        'hyper' : HyperMin
    }
    SketchType = sketch_types[args.sketch_type]
    print(f"Selected sketch type: {SketchType.__name__}")
    if args.sketch_type != 'all':
        print(f"Sketch size: {args.size}")
    print(f"kmer size: {args.k}")
    print()

    # ------------------------- Sketch computing starts here -------------------------

    print("--- Compute sketches ---")

    # Compute sketches
    sketches = []
    for idx, filepath in enumerate(files_to_load):
        print(f"loading {filepath}...")
        streamer = KmerStreamer(filepath, args.k)
        sketch = SketchType(kmer_streamer=streamer, name=path.basename(filepath))
        sketches.append(sketch)
        print(f"{idx+1}/{len(files_to_load)} files loaded.")

    print("All sketches loaded.")
    print()

    # Sketch comparisons
    print("--- Compute jaccard indexes ---")
    for sk1, sk2 in combinations(sketches, 2):
        print(f"Compare {sk1.name} with {sk2.name}")
        print(f"j={sk1.jaccard(sk2)}")