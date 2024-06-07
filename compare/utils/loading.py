from os import listdir, path


def load_fasta(filename):
    """ Loads a fasta formated file into a generator of sequences.
    :param str filename: The file to load
    """
    txt = []

    with open(filename) as fp:
        for line in fp:
            if line[0] == '>':
                if len(txt) > 0:
                    yield "".join(txt)
                txt = []
            else:
                txt.append(line.strip())

        if len(txt) > 0:
            yield "".join(txt)


# def load_directory(directory):
#     """ Loads all the fasta files from a directory
#     :param str directory: Path to the directory to load.
#     :return dict: A dict containing pairs filename: sequence array.
#     """
#     files = {}
#     for filename in listdir(directory):
#         if filename[filename.rfind('.')+1:] in ["fa", "fasta", "fna"]:
#             files[filename] = load_fasta(path.join(directory, filename))
    
#     return files


if __name__ == "__main__":
    files = load_directory("data")
    print(len(files))
