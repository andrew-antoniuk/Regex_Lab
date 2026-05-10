"""
Regex Lab
"""

#pylint: skip-file

from __future__ import annotations
from abc import ABC, abstractmethod

class State(ABC):

    @abstractmethod
    def __init__(self) -> None:
        self.next_states: list[State] = []
        self.epsilon_states: list[State] = []

    @abstractmethod
    def check_self(self, char: str) -> bool:
        """
        function checks whether occured character is handled by current state
        """
        pass

    def check_next(self, next_char: str) -> State | Exception:
        for state in self.next_states:
            if state.check_self(next_char):
                return state
        raise NotImplementedError("rejected string")


class StartState(State):
    next_states: list[State] = []

    def __init__(self):
        super().__init__()

    def check_self(self, char):
        return False

class TerminationState(State):
    def __init__(self):
        self.next_states = []
        self.epsilon_states = []

    def check_self(self, char: str) -> bool:
        return False # end of string


class DotState(State):
    """
    state for . character (any character accepted)
    """

    next_states: list[State] = []

    def __init__(self):
        self.next_states = []
        self.epsilon_states = []

    def check_self(self, char: str):
        return True # matches everything


class AsciiState(State):
    """
    state for alphabet letters or numbers
    """

    next_states: list[State] = []
    curr_sym = ""

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.next_states = []
        self.epsilon_states = []

    def check_self(self, curr_char: str) -> State | Exception:
        return curr_char == self.symbol

class StarState(State):

    next_states: list[State] = []

    def __init__(self, check_state: State):
        self.check_state = check_state
        self.next_states = []
        self.epsilon_states = []

    def check_self(self, char):
        # temp

        # for state in self.next_states:
        #     if state.check_self(char):
        #         return True

        return False

class PlusState(State):
    next_states: list[State] = []

    def __init__(self, check_state: State):
        self.check_state = check_state
        self.next_states = []
        self.epsilon_states = []

    def check_self(self, char):
        return False

class RegexFSM:
    curr_state: State = StartState()

    def __init__(self, regex_expr: str) -> None:

        prev_state = self.curr_state
        tmp_next_state = self.curr_state

        for char in regex_expr:
            tmp_next_state = self.__init_next_state(char, prev_state, tmp_next_state)
            prev_state.next_states.append(tmp_next_state)
            prev_state = tmp_next_state # temp

    def __init_next_state(
        self, next_token: str, prev_state: State, tmp_next_state: State
    ) -> State:
        new_state = None

        match next_token:
            case next_token if next_token == ".":
                new_state = DotState()
            case next_token if next_token == "*":
                new_state = StarState(tmp_next_state)
                # here you have to think, how to do it.

            case next_token if next_token == "+":
                pass  # Implement

            case next_token if next_token.isascii():
                new_state = AsciiState(next_token)

            case _:
                raise AttributeError("Character is not supported")

        return new_state

    def check_string(self, input_string: str) -> bool:
        states = {self.curr_state}

        for char in input_string:
            next_states = set()
            for state in states:
                # check transitions from the current state
                for t in state.next_states:
                    if t.check_self(char):
                        next_states.add(t)

            states = next_states
            if not states:
                return False

        return any(isinstance(s, TerminationState) for s in states)

if __name__ == "__main__":
    regex_pattern = "a*4.+hi"

    regex_compiled = RegexFSM(regex_pattern)

    print(regex_compiled.check_string("aaaaaa4uhi"))  # True
    print(regex_compiled.check_string("4uhi"))  # True
    print(regex_compiled.check_string("meow"))  # False
