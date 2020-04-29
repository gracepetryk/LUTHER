#!/usr/bin/env python3

from collections import deque
from itertools import islice
from typing import List, Union
import sys
import re
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
                        # read in the next 2 characters as a hex character code
                        self.alphabet += chr(int("".join(islice(index_range, 2)), 16))
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

    def tokenize_source(self):

        # record the location of each newline in a queue so we can know what line we're on.
        newline_indices = deque()
        newline_indices.appendleft(-1)  # needed to make sure character line position works
        for i, char in zip(range(len(self.input_text)), self.input_text):
            if char == '\n':
                newline_indices.appendleft(i)

        with open(self._output_path, 'w') as o:
            token_start_char = 1  # the line the current token starts on
            token_start_line = 1  # the character on that line the token starts on
            current_char_index = 0  # the character index in the input string the token starts on

            while current_char_index < len(self.input_text):

                # run all the dfa matching
                for dfa in self.dfa_list:
                    dfa.match(self.input_text, current_char_index)

                # find the best dfa, tie goes to first in list
                best_dfa: Union[DFA, None] = None
                for dfa in self.dfa_list:
                    if (best_dfa is None
                            or (len(dfa.longestPreviousMatch) > 0
                                and len(dfa.longestPreviousMatch) > len(best_dfa.longestPreviousMatch))):
                        # if the best_dfa is undefined or the current dfa is
                        # defined and longer than the best, update best
                        best_dfa = dfa

                # write token data to file
                o.write(best_dfa.identifier + " ")

                token = convert_escaped_chars(best_dfa.longestPreviousMatch) \
                    if best_dfa.token is None else best_dfa.token
                o.write(token + " ")

                o.write("{} {}".format(token_start_line, token_start_char))
                o.write("\n")

                # figure out the start character and line of next token
                current_char_index += len(best_dfa.longestPreviousMatch)

                last_newline = newline_indices.pop()
                next_newline = newline_indices.pop()

                while current_char_index > next_newline:
                    last_newline = next_newline
                    next_newline = newline_indices.pop() if newline_indices else len(self.input_text)
                    token_start_line += 1

                newline_indices.append(next_newline)
                newline_indices.append(last_newline)

                # plus one because current char and last newline are both 0 indexed while token start is 1 indexed
                token_start_char = current_char_index - last_newline

    def __read_dfa(self, line: str) -> DFA:
        params = line.split()
        file_name = params[0]
        identifier = params[1]
        token = params[2] if len(params) > 2 else None  # only read in token if provided

        try:
            with open(file_name, 'r') as file:
                lines = file.read().splitlines()
                return DFA(identifier, token, self.alphabet, lines)
        except IOError:
            sys.exit(1)


def convert_escaped_chars(input_str: str) -> str:
    """
    converts a regular string with escaped chars and spaces to fit the LUTHER format
    :param input_str:
    :return:
    """

    output_str = ""
    allowed_char = re.compile("[A-Za-wy-z0-9]")
    for char in input_str:
        if allowed_char.match(char):
            output_str += char
        else:
            output_str += "{0:#0{1}x}".format(ord(char), 4)[1:]

    return output_str


def main():

    luther = LUTHER(sys.argv[1], sys.argv[2], sys.argv[3])
    luther.tokenize_source()

    sys.exit()


if __name__ == "__main__":
    main()

