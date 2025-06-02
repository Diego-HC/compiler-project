# Compiler Phases and Implementation

This document explains the different phases of the compiler/interpreter implementation and links them to specific parts of the code in `CompilerProgram.py`.

## Overview

The implementation follows the traditional compiler architecture with three main phases:
1. **Lexical Analysis (Lexer/Tokenizer)**
2. **Syntax Analysis (Parser)**
3. **Execution (Interpreter/Code Generation)**

## Phase 1: Lexical Analysis

### Purpose
The lexical analyzer (lexer) breaks down the input source code into a sequence of tokens. It's the first phase of compilation that converts the character stream into meaningful symbols.

### Implementation: `BasicLexer` Class

**Location in code:** Lines 6-40

```python
class BasicLexer(Lexer):
```

#### Token Definitions

**Token Set (Line 7):**
```python
tokens = {NAME, NUMBER, STRING, IF, THEN, ELSE, ENDIF}
```

**Character Literals (Line 9):**
```python
literals = {"=", "+", "-", "/", "*", "(", ")", ",", ";", "<", ">", "!"}
```

**Ignored Characters (Line 8):**
```python
ignore = "\t "  # Ignores tabs and spaces
```

#### Token Recognition Patterns

**Keywords (Lines 13-16):**
- `IF = r"if"`
- `THEN = r"then"`
- `ELSE = r"else"`
- `ENDIF = r"endif"`

**Identifiers (Line 19):**
```python
NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"
```
- Matches variable names starting with letter/underscore followed by alphanumeric characters

**String Literals (Line 20):**
```python
STRING = r"\".*?\""
```
- Matches quoted strings with non-greedy matching

**Number Token with Action (Lines 23-27):**
```python
@_(r"\d+")
def NUMBER(self, t):
    t.value = int(t.value)  # Convert to integer
    return t
```

**Comment Handling (Lines 29-32):**
```python
@_(r"//.*")
def COMMENT(self, t):
    pass  # Ignore comments
```

**Line Number Tracking (Lines 34-37):**
```python
@_(r"\n+")
def newline(self, t):
    self.lineno = t.value.count("\n")
```

### Lexer Features
- **Token Recognition**: Converts character sequences into meaningful tokens
- **Keyword Detection**: Distinguishes between keywords and identifiers
- **Number Conversion**: Automatically converts numeric strings to integers
- **Comment Filtering**: Removes comments from the token stream
- **Whitespace Handling**: Ignores spaces and tabs
- **Line Tracking**: Maintains line numbers for error reporting

## Phase 2: Syntax Analysis (Parsing)

### Purpose
The parser takes the token stream from the lexer and builds an Abstract Syntax Tree (AST) based on the grammar rules. It checks if the input follows the correct syntax.

### Implementation: `BasicParser` Class

**Location in code:** Lines 42-122

```python
class BasicParser(Parser):
```

#### Grammar Rules and AST Construction

**Token Import (Line 44):**
```python
tokens = BasicLexer.tokens
```

**Operator Precedence (Lines 46-53):**
```python
precedence = (
    ("left", "<", ">"),           # Comparison operators
    ("left", "IF", "THEN", "ELSE", "ENDIF"),  # Conditional keywords
    ("left", "+", "-"),           # Addition/Subtraction
    ("left", "*", "/"),           # Multiplication/Division
    ("right", "UMINUS"),          # Unary minus
)
```

#### Production Rules

**Statement Rules (Lines 58-69):**

1. **Empty Statement:**
```python
@_("")
def statement(self, p):
    pass
```

2. **If Statement:**
```python
@_("if_stmt")
def statement(self, p):
    return p.if_stmt
```

3. **Variable Assignment:**
```python
@_("var_assign")
def statement(self, p):
    return p.var_assign
```

**Variable Assignment Rules (Lines 71-78):**

1. **Assign Expression to Variable:**
```python
@_('NAME "=" expr')
def var_assign(self, p):
    return ("var_assign", p.NAME, p.expr)
```

2. **Assign String to Variable:**
```python
@_('NAME "=" STRING')
def var_assign(self, p):
    return ("var_assign", p.NAME, p.STRING)
```

**Expression Rules (Lines 84-110):**

1. **Parenthesized Expression:**
```python
@_('"(" expr ")"')
def expr(self, p):
    return p.expr
```

2. **Binary Arithmetic Operations:**
```python
@_('expr "+" expr')
def expr(self, p):
    return ("add", p.expr0, p.expr1)

@_('expr "-" expr')
def expr(self, p):
    return ("sub", p.expr0, p.expr1)

@_('expr "*" expr')
def expr(self, p):
    return ("mul", p.expr0, p.expr1)

@_('expr "/" expr')
def expr(self, p):
    return ("div", p.expr0, p.expr1)
```

3. **Comparison Operations:**
```python
@_('expr "<" expr')
def expr(self, p):
    return ("lt", p.expr0, p.expr1)

@_('expr ">" expr')
def expr(self, p):
    return ("gt", p.expr0, p.expr1)
```

**Conditional Statement Rules (Lines 112-118):**

1. **Simple If Statement:**
```python
@_("IF expr THEN statement ENDIF")
def if_stmt(self, p):
    return ("if", p.expr, p.statement, None)
```

2. **If-Else Statement:**
```python
@_("IF expr THEN statement ELSE statement ENDIF")
def if_stmt(self, p):
    return ("if", p.expr, p.statement0, p.statement1)
```

**Terminal Expressions (Lines 114-122):**

1. **Unary Minus:**
```python
@_('"-" expr %prec UMINUS')
def expr(self, p):
    return p.expr
```

2. **Variable Reference:**
```python
@_("NAME")
def expr(self, p):
    return ("var", p.NAME)
```

3. **Number Literal:**
```python
@_("NUMBER")
def expr(self, p):
    return ("num", p.NUMBER)
```

### Parser Features
- **Grammar-Based Parsing**: Uses production rules to define language syntax
- **AST Generation**: Creates tree structures representing program semantics
- **Precedence Handling**: Correctly handles operator precedence and associativity
- **Error Recovery**: Built-in error handling from SLY framework
- **Left Recursion**: Handles left-recursive grammar rules efficiently

## Phase 3: Execution (Interpreter)

### Purpose
The interpreter traverses the AST generated by the parser and executes the program by evaluating expressions and managing program state.

### Implementation: `BasicExecute` Class

**Location in code:** Lines 124-184

```python
class BasicExecute:
```

#### Tree Walking Interpreter

**Constructor (Lines 126-132):**
```python
def __init__(self, tree, env):
    self.env = env
    result = self.walkTree(tree)
    if result is not None and isinstance(result, int):
        print(result)
    if isinstance(result, str) and result[0] == '"':
        print(result)
```

**Main Execution Method (Lines 134-184):**

#### Base Cases

**Primitive Values (Lines 136-142):**
```python
if isinstance(node, int):
    return node
if isinstance(node, str):
    return node
if node is None:
    return None
```

#### Node Type Handlers

**Number Literals (Lines 152-153):**
```python
if node[0] == "num":
    return node[1]
```

**String Literals (Lines 155-156):**
```python
if node[0] == "str":
    return node[1]
```

**Arithmetic Operations (Lines 158-165):**
```python
if node[0] == "add":
    return self.walkTree(node[1]) + self.walkTree(node[2])
elif node[0] == "sub":
    return self.walkTree(node[1]) - self.walkTree(node[2])
elif node[0] == "mul":
    return self.walkTree(node[1]) * self.walkTree(node[2])
elif node[0] == "div":
    return self.walkTree(node[1]) / self.walkTree(node[2])
```

**Comparison Operations (Lines 167-170):**
```python
if node[0] == "lt":
    return self.walkTree(node[1]) < self.walkTree(node[2])
elif node[0] == "gt":
    return self.walkTree(node[1]) > self.walkTree(node[2])
```

**Conditional Execution (Lines 172-179):**
```python
if node[0] == "if":
    condition = self.walkTree(node[1])
    print("Condition evaluated to:", condition)
    print("node", node)
    if condition:
        return self.walkTree(node[2])  # then branch
    elif node[3] is not None:
        return self.walkTree(node[3])  # else branch
```

**Variable Operations (Lines 181-190):**

1. **Variable Assignment:**
```python
if node[0] == "var_assign":
    self.env[node[1]] = self.walkTree(node[2])
    return node[1]
```

2. **Variable Lookup:**
```python
if node[0] == "var":
    try:
        return self.env[node[1]]
    except LookupError:
        print("Undefined variable '" + node[1] + "' found!")
        return 0
```

### Interpreter Features
- **Tree Traversal**: Recursive evaluation of AST nodes
- **Environment Management**: Symbol table for variable storage
- **Type Handling**: Support for integers and strings
- **Error Handling**: Graceful handling of undefined variables
- **Interactive Feedback**: Debug output for conditional evaluation

## Phase 4: Main Program Loop

### Purpose
Provides the interactive Read-Eval-Print Loop (REPL) that ties all compiler phases together.

### Implementation: Main Program

**Location in code:** Lines 187-235

#### Program Initialization (Lines 192-200):**
```python
if __name__ == "__main__":
    lexer = BasicLexer()
    parser = BasicParser()
    print("TC3002B Programming Language Program 1.0 ...")
    print('Type "help", "credits" or "exit" to exit the program.')
    env = {}
```

#### Interactive Loop (Lines 202-235):**

**Input Processing:**
```python
while True:
    try:
        text = input(">> ")
    except EOFError:
        break
```

**Command Handling (Lines 209-224):**
```python
if text.strip().lower() in ("exit", "quit"):
    break
elif text.strip().lower() == "help":
    print("This is a simple interpreter...")
    continue
elif text.strip().lower() == "credits":
    print("Developed by Ivan Romero...")
    continue
```

**Compilation Pipeline (Lines 233-234):**
```python
tree = parser.parse(lexer.tokenize(text))
BasicExecute(tree, env)
```

## Data Flow Through Phases

1. **User Input** → Raw source code string
2. **Lexical Analysis** → Token stream
3. **Syntax Analysis** → Abstract Syntax Tree (AST)
4. **Execution** → Program execution with side effects

### Example Data Flow

**Input:** `x = 5 + 3`

1. **Lexer Output:**
   - `NAME('x'), '=', NUMBER(5), '+', NUMBER(3)`

2. **Parser Output (AST):**
   - `('var_assign', 'x', ('add', ('num', 5), ('num', 3)))`

3. **Interpreter Execution:**
   - Evaluates `('add', ('num', 5), ('num', 3))` → `8`
   - Stores `x = 8` in environment
   - Returns `'x'`

## Architecture Benefits

1. **Modularity**: Clear separation of concerns between phases
2. **Extensibility**: Easy to add new tokens, grammar rules, or operations
3. **Maintainability**: Each phase can be modified independently
4. **Debugging**: Clear data flow makes debugging easier
5. **Reusability**: Components can be reused for different language variants

## Integration with SLY Framework

The implementation leverages the SLY (SLY Lex-Yacc) framework:

- **Lexer**: Inherits from `sly.Lexer` for token recognition
- **Parser**: Inherits from `sly.Parser` for grammar-based parsing
- **Decorators**: Uses `@_()` decorators to define grammar rules
- **Automatic AST**: SLY automatically constructs parse trees
- **Error Handling**: Built-in error recovery mechanisms

This architecture provides a solid foundation for a compiler/interpreter while remaining simple enough for educational purposes.
