#!/usr/bin/env python3
from more_itertools import consume
from itertools import islice
from typing import List, Set
import sys
from dfa import DFA


class LUTHER:
    def __init__(self, scan_def_path, src_path, output_path):
        self._output_path = output_path
        self.alphabet: List[chr] = []
        self.dfa_list: List[DFA] = []
        self.input_text: str

        # read in scanning definition
        try:
            with open(scan_def_path, 'r') as f:
                file_lines = f.readlines()

                # read in header
                header = file_lines[0]
                index_range = iter(header)
                for i in index_range:
                    # read in first line information
                    if i in [' ', '\n', '\t']:
                        continue
                    if i == 'x':
                        self.alphabet += chr(int("".join(islice(index_range, 2)), 16))
                        consume(header, 2)  # skip the next two characters
                    else:
                        self.alphabet.append(i)

                # initialize DFAs
                for line in file_lines[1:]:
                    if len(line.strip()) == 0:
                        continue

                    self.dfa_list.append(self.__read_dfa(line))

                if len(self.dfa_list) == 0:
                    sys.exit(1)

            with open(src_path, 'r') as f:
                self.input_text = "".join(f.readlines())

        except IOError:
            sys.exit(1)

    def __read_dfa(self, line: str) -> DFA:
        params = line.split()
        file_name = params[0]
        identifier = params[1]
        token = params[2] if len(params) > 2 else None

        try:
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                return DFA(identifier, token, self.alphabet, lines)
        except IOError:
            sys.exit(1)


def main():

    luther = LUTHER(sys.argv[1], sys.argv[2], sys.argv[3])
    print(luther)

    sys.exit()


if __name__ == "__main__":
    main()

