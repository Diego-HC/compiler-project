# TC3002B Programming Language - User Manual

## Overview

This is a simple interpreter for a basic programming language developed by Ivan Romero (A00833623) and Diego Hernandez (A00834015). The interpreter supports variables, arithmetic operations, comparison operations, and conditional statements.

## Installation and Usage

### Prerequisites
- Python 3.x
- SLY (SLY Lex-Yacc) library

### Installation
```bash
pip install sly
```

### Running the Interpreter
```bash
python CompilerProgram.py
```

## Language Features

### 1. Data Types

#### Numbers
- Integer values are supported
- Examples: `42`, `0`, `-15`

#### Strings
- String literals enclosed in double quotes
- Examples: `"hello"`, `"world"`, `"123"`

#### Variables
- Variable names must start with a letter or underscore
- Can contain letters, numbers, and underscores
- Examples: `x`, `counter`, `my_var`, `_temp`

### 2. Operators

#### Arithmetic Operators
- `+` : Addition
- `-` : Subtraction
- `*` : Multiplication
- `/` : Division
- `-` : Unary minus (negation)

#### Comparison Operators
- `<` : Less than
- `>` : Greater than

#### Assignment Operator
- `=` : Variable assignment

### 3. Language Constructs

#### Variable Assignment
```
variable_name = expression
variable_name = "string"
```

Examples:
```
x = 5
name = "John"
result = x + 10
```

#### Arithmetic Expressions
```
5 + 3
10 - 4
6 * 7
20 / 4
(5 + 3) * 2
```

#### Comparison Expressions
```
5 > 3
10 < 20
x > y
```

#### Conditional Statements

**Simple If Statement:**
```
if condition then statement endif
```

**If-Else Statement:**
```
if condition then statement else statement endif
```

Examples:
```
if x > 5 then y = 10 endif
if x > 0 then y = 1 else y = 0 endif
```

## Interactive Commands

### Built-in Commands
- `help` : Display help information
- `credits` : Show developer credits
- `exit` or `quit` : Exit the interpreter

### Usage Examples

#### Basic Arithmetic
```
>> 5 + 3
8
>> 10 * 2
20
>> (15 + 5) / 4
5.0
```

#### Variable Operations
```
>> x = 10
x
>> y = 5
y
>> x + y
15
>> result = x * y
result
>> result
50
```

#### String Operations
```
>> name = "Alice"
name
>> greeting = "Hello"
greeting
```

#### Conditional Logic
```
>> x = 10
x
>> if x > 5 then y = 100 endif
>> y
100
>> if x < 5 then z = 1 else z = 2 endif
>> z
2
```

## Error Handling

### Undefined Variables
If you try to use a variable that hasn't been defined, the interpreter will display an error message and return 0:
```
>> undefined_var
Undefined variable 'undefined_var' found!
0
```

### Syntax Errors
Invalid syntax will cause the parser to fail. Make sure to follow the correct syntax for each construct.

## Operator Precedence

The operators follow standard mathematical precedence (from highest to lowest):
1. Unary minus (`-`)
2. Multiplication and Division (`*`, `/`)
3. Addition and Subtraction (`+`, `-`)
4. Comparison operators (`<`, `>`)
5. Conditional statements (`if`, `then`, `else`, `endif`)

Use parentheses to override default precedence:
```
>> 2 + 3 * 4
14
>> (2 + 3) * 4
20
```

## Tips and Best Practices

1. **Variable Naming**: Use descriptive variable names to make your code more readable
2. **Parentheses**: Use parentheses to make complex expressions clearer
3. **Testing**: Test your conditional statements with different values
4. **Spacing**: The interpreter ignores spaces and tabs, so use them for readability

## Limitations

- Only integer and string data types are supported
- Limited set of comparison operators (only `<` and `>`)
- No loop constructs (while, for)
- No function definitions
- No complex data structures (arrays, objects)
- Division results in floating-point numbers
- No equality operator (`==`)

## Examples Session

```
TC3002B Programming Language Program 1.0 (tags/v3.10.11:7d4cc5a, Jun 1 2025, 00:38:17
Type "help", "credits" or "exit" to exit the program.
>> x = 10
x
>> y = 5
y
>> sum = x + y
sum
>> sum
15
>> if sum > 10 then message = "Large sum" else message = "Small sum" endif
>> message
"Large sum"
>> product = x * y
product
>> product
50
>> if product > 40 then result = 1 endif
>> result
1
>> exit
```
