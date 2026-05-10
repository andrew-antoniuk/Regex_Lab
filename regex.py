"""
Regex Lab
"""

from __future__ import annotations
from abc import ABC, abstractmethod

class State(ABC):

    """
    Abstract base class for all FSM states.
    Derived classes define how a particular symbol is recognized.
    """

    @abstractmethod
    def __init__(self) -> None:
        self.next_states: list[State] = []
        self.epsilon_states: list[State] = []

    @abstractmethod
    def check_self(self, char: str) -> bool:
        """
        function checks whether occured character is handled by current state
        """

    def check_next(self, next_char: str) -> State | Exception:

        """
        Find the next reachable state for the given character.
        The method iterates through outgoing transitions and returns the first matching state.
        """

        for state in self.next_states:
            if state.check_self(next_char):
                return state
        raise NotImplementedError("rejected string")

class StartState(State):

    """
    Initial state of the finite-state machine.
    This state does not consume characters and only serves as an entry point into the automaton
    """

    next_states: list[State] = []

    def __init__(self):
        super().__init__()

    def check_self(self, char):

        """
        Start state never directly accepts characters.
        Character processing begins from its outgoing transitions.
        """

        return False

class TerminationState(State):

    """
    Final accepting state of the automaton.
    Reaching this state after processing the whole input means that the string is accepted.
    """

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

    def check_self(self, char: str) -> State | Exception:
        return char == self.symbol

class StarState(State):

    """
    Helper state for handling the '*' regex operator.
    The operator allows zero or more repetitions of the previous expression.
    """

    next_states: list[State] = []

    def __init__(self, check_state: State):
        self.check_state = check_state
        self.next_states = []
        self.epsilon_states = []

    def check_self(self, char):

        # for state in self.next_states:
        #     if state.check_self(char):
        #         return True

        return False

class PlusState(State):

    """
    Helper state for handling the '+' regex operator.
    The operator allows one or more repetitions of the previous expression.
    """

    next_states: list[State] = []

    def __init__(self, check_state: State):
        self.check_state = check_state
        self.next_states = []
        self.epsilon_states = []

    def check_self(self, char):
        return False

class RegexFSM:

    """
    Regex compiler and finite-state machine executor.
    The class converts a regex expression into connected states and validates input strings.
    """
    # curr_state: State = StartState()

    def __init__(self, regex_expr: str) -> None:
        self.curr_state = StartState()
        prev_state = self.curr_state
        tmp_next_state = self.curr_state

        for char in regex_expr:
            tmp_next_state = self.__init_next_state(char, prev_state, tmp_next_state)
            if tmp_next_state is not None: # logic fix
                prev_state.next_states.append(tmp_next_state)
                prev_state = tmp_next_state # redefine

        t = TerminationState()
        prev_state.epsilon_states.append(t)

    def __init_next_state(
        self, next_token: str, prev_state: State, tmp_next_state: State
    ) -> State:
        new_state = None

        match next_token:
            case next_token if next_token == ".":
                new_state = DotState()

            case next_token if next_token == "*":
                prev_state.next_states.append(prev_state)

                self.curr_state.epsilon_states.append(prev_state)

                return None

            case next_token if next_token == "+":
                tmp_next_state.next_states.append(tmp_next_state)
                return None

            case next_token if next_token.isascii():
                new_state = AsciiState(next_token)

            case _:
                raise AttributeError("Character is not supported")

        return new_state

    def check_string(self, input_string: str) -> bool:

        """
        Validate an input string using FSM traversal
        """

        states = self.epsilon_f({self.curr_state})

        for char in input_string:
            next_states = set()
            for state in states:
                for n in state.next_states:
                    if n.check_self(char):
                        next_states.update(self.epsilon_f({n}))

            states = next_states
            if not states:
                return False

        states = self.epsilon_f(states)
        return any(isinstance(s, TerminationState) for s in states)

    def epsilon_f(self, states):

        """
        Compute epsilon-closure for a set of states.
        The closure contains all states reachable without consuming additional characters.
        """

        c, stack = set(states), list(states)
        while stack:
            state = stack.pop()
            for s in state.epsilon_states:
                if s not in c:
                    c.add(s)
                    stack.append(s)
        return c

if __name__ == "__main__":
    regex_pattern = "a*4.+hi"

    regex_compiled = RegexFSM(regex_pattern)

    print(regex_compiled.check_string("aaaaaa4uhi"))  # True
    print(regex_compiled.check_string("4uhi"))  # True
    print(regex_compiled.check_string("meow"))  # False
