"""
Tests only
"""

from regex import RegexFSM

if __name__ == "__main__":

    # create a pattern according to the limitations
    R1 = "a*4.+hi"

    # compile it using Regex FSM compiler
    regex_compiled = RegexFSM(R1)

    # run the FSM compiler with various inputs
    print(regex_compiled.check_string("aaaaaa4uhi"))  # True
    print(regex_compiled.check_string("4uhi"))  # True
    print(regex_compiled.check_string("meow"))  # False

    R2 = "abc"
    regex_compiled = RegexFSM(R2)
    print(regex_compiled.check_string("abc"))  # True
    print(regex_compiled.check_string("a"))  # False

    R3 = "A9.*z+"
    regex_compiled = RegexFSM(R3)
    print(regex_compiled.check_string("A9helloz"))  # True
    print(regex_compiled.check_string("A9123zzzz")) # True
    print(regex_compiled.check_string("A9_test_z")) # True
