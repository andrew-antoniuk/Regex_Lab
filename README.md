# Regex_Lab

A small regex engine implemented using FSM.
The project compiles a simplified regex expression into a graph of connected states and validates strings by traversing this graph.

The engine currently supports:

| Operator | Meaning |
|---|---|
| `a-z`, `A-Z`, `0-9` | Exact symbol match |
| `.` | Any character |
| `*` | Zero or more repetitions |
| `+` | One or more repetitions |

---

## State System

Each regex token is represented as a state object.

### Main State Types

- `StartState`: Entry point of the automaton

- `AsciiState`: Matches a specific alphanumeric character

- `DotState`: Matches any character

- `TerminationState`: Final accepting state

- `StarState`, `PlusState`: Helper states used during regex compilation

---

# How It Works

## 1. Regex Compilation

The regex expression is converted into a graph of connected states.

`a*4.+hi` becomes conceptually:

```text
START
  |
  v
[a] --loop--
 | \
 |  \  epsilon
 |   \
 v    v
[4] -> [.] --loop--> [h] -> [i] -> END
```

### Operators

#### `*`

Creates: self-loopepsilon, transition

`a*` allows:

```text
"", "a", "aa", "aaa", ...
```

---

#### `+`

Creates: self-loop only

`a+` allows:

```text
"a", "aa", "aaa", ...
```

but not an empty string.

---

## 2. String Validation

The FSM traverses all currently reachable states while processing the input string character-by-character.

The algorithm:
1. Computes epsilon-closure
2. Finds matching transitions
3. Moves to next states
4. Repeats for all characters

The string is accepted if the automaton reaches `TerminationState`.

---

# Example Usage

```python
# create a pattern
regex_pattern = "a*4.+hi"

# compile it using Regex FSM Compiler
regex_compiled = RegexFSM(regex_pattern)

# Input strings
print(regex_compiled.check_string("aaaaaa4uhi"))
print(regex_compiled.check_string("4uhi"))
print(regex_compiled.check_string("meow"))

# Recieve boolean results(each corresponds to the specific string telling if it was readed)
```

Output:

```text
True
True
False
```

---

# Example Patterns

## Basic Exact Match

`abc` matches `abc`

---

## Wildcard

`a.c` matches `abc axc a5c`

---

## Zero or More

`ab*c` matches `ac abc abbc abbbbbc`

---

## One or More

`ab+c` matches `abc abbc abbbbbc` and does NOT match `ac`

---

## Digits

`123+` matches `123 1233 1233333`

---

## Mixed Pattern

`A9.*z+` matches `A9helloz A9123zzzz A9_test_z`

---

The engine does not yet support parentheses `()`, alternation `|`, character classes `[]`, escaped characters etc.
