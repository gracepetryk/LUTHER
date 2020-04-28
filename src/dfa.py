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
        self.matchState = DFAMatchState.WILL_NOT_MATCH
        self.longestPreviousMatch = ""
        self.identifier = identifier
        self.token = token

        # create the DFA States
        for line in tt_lines:
            line_chars = line.split()
            accepting = line_chars[0] == '+'
            transitions = line_chars[2:].copy()
            self._states.append(_DFAState(self, transitions, accepting))

    def match(self, input_str):
        """
        gets the longest possible match for a given input string
        :param input_str:
        """
        self._reset()

        current_state = self._states[0]
        index = 0
        current_char = input_str[0]
        match = ""

        while current_state.can_match(current_char):
            match += current_char

            if current_state.accepting:
                self.matchState = DFAMatchState.MATCHING
                if len(match) > len(self.longestMatch):
                    self.longestPreviousMatch = match
            else:
                self.matchState = DFAMatchState.WILL_NOT_MATCH

            index += 1
            current_state = self._states[index]
            current_char = input_str[index]

    def _reset(self):
        self.matchState = DFAMatchState.WILL_NOT_MATCH
        self.longestMatch = ""


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
                self.transitions[transition[0]] = transition[1]

    def can_match(self, char: str) -> bool:
        return char in self.transitions.keys()
