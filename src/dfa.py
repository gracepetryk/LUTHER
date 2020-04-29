from enum import Enum
from typing import List


class DFA:
    def __init__(self, identifier: str, token: str, alphabet: List[chr], tt_lines: List[str]):
        """

        :param identifier:
        :param token:
        :param alphabet:
        :param tt_lines:
        """
        self._states = []
        self.alphabet = alphabet
        self.longestPreviousMatch = ""
        self.identifier = identifier
        self.token = token

        # create the DFA States
        for line in tt_lines:
            line_chars = line.split()
            accepting = line_chars[0] == '+'
            transitions = line_chars[2:].copy()
            self._states.append(_DFAState(self, transitions, accepting))

    def match(self, input_str, start_index=0):
        """
        gets the longest possible match for a given input string
        :param input_str:
        :param start_index: the index to start tokenizing at (default 0)
        """
        self._reset()

        current_state = self._states[0]
        index_in_input = start_index
        current_char = input_str[start_index]
        match = ""

        while current_state.can_match(current_char):
            match += current_char
            current_state = self._states[current_state.get_transition_index(current_char)]

            if current_state.accepting:
                if len(match) > len(self.longestPreviousMatch):
                    self.longestPreviousMatch = match

            index_in_input += 1
            if index_in_input < len(input_str):
                current_char = input_str[index_in_input]
            else:
                # return when EOF reached
                return

    def _reset(self):
        self.longestPreviousMatch = ""


class DFAMatchState(Enum):
    MATCHING = 1
    WILL_NOT_MATCH = 2


class _DFAState:

    def __init__(self, dfa: DFA, tt_line, accepting):
        """
        :param dfa: the dfa this node belongs to
        :param tt_line: the transitions to other nodes contained in this dfa, in the order of the alphabet
        """

        self.transitions: dict = {}
        self.accepting = accepting

        # populate transitions for dfa state
        for transition in zip(dfa.alphabet, tt_line):
            if transition[1] != 'E':
                self.transitions[transition[0]] = int(transition[1])

    def can_match(self, char: str) -> bool:
        return char in self.transitions.keys()

    def get_transition_index(self, char: str) -> int:
        return self.transitions[char]
