#!/usr/bin/env python
#
# Picaro: An simple command-line alignment visualization tool.
#
# picaro.py
# Visualize alignments between sentences in a grid format.
#
# Jason Riesa <riesa@isi.edu>
# version: 01-16-2010

import sys, os
from collections import defaultdict

a1_file_str = ""
a2_file_str = ""
f_file_str = ""
e_file_str = ""
maxlen = float('inf')

def main(args):
    for sentenceNumber, line in enumerate(sys.stdin):
        fields = line.rstrip().split("\t")

        src, trg, aline = fields[0:3]
        a2Line = None
        if len(fields) == 4:
            a2line = fields[3]
            links2 = a2line.split()

        links = aline.split()
        src_words = src.split()
        trg_words = trg.split()

        # Don't generate alignment grids for very large sentences
        if len(trg_words) > maxlen or len(src_words) > maxlen:
            continue

        a = defaultdict(lambda: defaultdict(int))
        a2 = defaultdict(lambda: defaultdict(int))

        # Print source words on the columns
        # First, find the length of the longest word
        longestEWordSize = 0
        longestEWord = 0
        for w in trg_words:
            if len(w) > longestEWordSize:
                longestEWordSize = len(w)
                longestEWord = w

        # Now, print the e-words
        for i in range(longestEWordSize, 0, -1):
            for w in trg_words:
                if len(w) < i:
                    print("  ", end="")
                else:
                    print(w[(i*-1)], "", end="")
            print()

        # Fill in alignment matrix 1
        for link in links:
            i, j = map(int, link.split('-'))
            a[int(i)][int(j)] = 1

        # Fill in alignment matrix 2
        if a2Line is not None:
            for link in links2:
                i, j = map(int, link.split('-'))
                a2[i][j] = 1

            for i, _ in enumerate(src_words):
                for j, _ in enumerate(trg_words):
                    val1 = a[i][j]
                    if val1 == 0:
                        # No link
                        print(': ', end="")
                    elif val1 == 1:
                        # Regular link
                        print(u'\u001b[44m\u0020\u001b[0m ', end="")
                    elif val1 == 2:
                        # Link due to transitive closure
                        # Render as gray-shaded square
                        print('O', end="")
                print(src_words[i])
            print
        else:
            for i, _ in enumerate(src_words):
                for j, _ in enumerate(trg_words):
                    val1 = a[i][j]
                    val2 = a2[i][j]

                    if val1 == 0 and val2 == 0:
                        # Link not in a nor a2
                        # Empty grid box
                        print(': ', end="")
                    # Link in both a and a2
                    elif val1 > 0 and val2 > 0:
                        # Green box
                        if val1 == 1:
                            if val2 == 1:
                                print(u'\u001b[42m\u001b[1m\u0020\u001b[0m ', end="")
                            elif val2 == 2:
                                print(u'\u001b[42m\u001b[30m2\u001b[0m ', end="")
                        elif val1 == 2:
                            if val2 == 1:
                                print(u'\u001b[42m\u0020\u001b[0m ', end="")
                            elif val2 == 2:
                                print(u'\u001b[42m\u001b[30m3\u001b[0m ', end="")
                    # Link in a2, but not a
                    elif val1 == 0 and val2 > 0:
                        if val2 == 1:
                            # Yellow box
                            print(u'\u001b[1m\u001b[43m\u0020\u001b[0m ', end="")
                        elif val2 == 2:
                            # Artificial link by transitive closure
                            print(u'\u001b[43m\u001b[30m2\u001b[0m ', end="")

                    # Link in a, but not a2
                    elif val1 > 0 and val2 == 0:
                        if val1 == 1:
                            # Blue box
                            print(u'\u001b[1m\u001b[44m\u0020\u001b[0m ', end="")
                        elif val1 == 2:
                            print(u'\u001b[44m\u001b[37m1\u001b[0m ', end="")
                print(src_words[i])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Visualize alignments between sentences in a grid format.')
    parser.add_argument('--maxlen', "-m", type=int, help='display alignment only when e and f have length <= len')
    args = parser.parse_args()

    main(args)
