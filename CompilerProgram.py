# Building a Lexer - Tokenizer

from sly import Lexer, Parser
import sys
import os


# Class lexer using sly's lexer
class BasicLexer(Lexer):
    tokens = {NAME, NUMBER, STRING, IF, THEN, ELSE, ENDIF, WHILE, DO, ENDWHILE}
    ignore = "\t "
    # Define the literals used in the language
    # These are the symbols that are not keywords but are used in expressions
    literals = {"=", "+", "-", "/", "*", "(", ")", ",", ";", "<", ">", "!"}

    # Define tokens as regular expressions

    # Keywords
    # These are the reserved words in the language
    # They cannot be used as identifiers
    IF = r"if"
    THEN = r"then"
    ELSE = r"else"
    ENDIF = r"endif"
    WHILE = r"while"
    DO = r"do"
    ENDWHILE = r"endwhile"

    # Identifiers and strings
    # Identifiers' first character must be a letter or underscore, followed by letters, digits, or underscores
    NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"
    STRING = r"\".*?\""

    # Number token
    @_(r"\d+")
    def NUMBER(self, t):
        # convert it into a python integer
        # right now the regex only matches integers not floats
        t.value = int(t.value)
        return t

    # Comment token
    @_(r"//.*")
    def COMMENT(self, t):
        pass

    # Newline token (used only for showing errors in new line)
    @_(r"\n+")
    def newline(self, t):
        self.lineno = t.value.count("\n")


class BasicParser(Parser):
    # tokens are passed from lexer to parser
    tokens = BasicLexer.tokens

    # Define precedence of operators
    # This defines the order of operations for the language
    precedence = (
        ("left", "+", "-"),
        ("left", "*", "/"),
        ("right", "UMINUS"),
    )

    def __init__(self):
        self.env = {}

    # Define the grammar rules
    @_("")
    def statement(self, p):
        pass

    @_("if_stmt")
    def statement(self, p):
        return p.if_stmt

    @_("while_stmt")
    def statement(self, p):
        return p.while_stmt

    @_("var_assign")
    def statement(self, p):
        return p.var_assign

    @_('NAME "=" expr')
    def var_assign(self, p):
        return ("var_assign", p.NAME, p.expr)

    @_('NAME "=" STRING')
    def var_assign(self, p):
        return ("var_assign", p.NAME, p.STRING)

    @_("expr")
    def statement(self, p):
        return p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

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

    @_('expr "<" expr')
    def expr(self, p):
        return ("lt", p.expr0, p.expr1)

    @_('expr ">" expr')
    def expr(self, p):
        return ("gt", p.expr0, p.expr1)

    @_("IF expr THEN statement ENDIF")
    def if_stmt(self, p):
        return ("if", p.expr, p.statement, None)

    @_("IF expr THEN statement ELSE statement ENDIF")
    def if_stmt(self, p):
        return ("if", p.expr, p.statement0, p.statement1)

    @_("WHILE expr DO statement ENDWHILE")
    def while_stmt(self, p):
        return ("while", p.expr, p.statement)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_("NAME")
    def expr(self, p):
        return ("var", p.NAME)

    @_("NUMBER")
    def expr(self, p):
        return ("num", p.NUMBER)


class BasicExecute:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == "program":
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == "num":
            return node[1]

        if node[0] == "str":
            return node[1]

        if node[0] == "add":
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == "sub":
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == "mul":
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == "div":
            return self.walkTree(node[1]) / self.walkTree(node[2])

        if node[0] == "lt":
            return self.walkTree(node[1]) < self.walkTree(node[2])
        elif node[0] == "gt":
            return self.walkTree(node[1]) > self.walkTree(node[2])

        if node[0] == "if":
            condition = self.walkTree(node[1])
            print("Condition evaluated to:", condition)
            if condition:
                return self.walkTree(node[2])  # then branch
            elif node[3] is not None:
                return self.walkTree(node[3])  # else branch

        if node[0] == "while":
            while self.walkTree(node[1]):
                self.walkTree(node[2])
            return None

        if node[0] == "var_assign":
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == "var":
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '" + node[1] + "' found!")
                return 0


def execute_file(filename):
    """Execute code from a file by using: python CompilerProgram.py <filename> or ./compiler <filename>"""
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return

    try:
        with open(filename, "r") as file:
            content = file.read()

        lexer = BasicLexer()
        parser = BasicParser()
        env = {}

        print(f"Executing file: {filename}")
        print("-" * 40)

        # Split content into lines and execute each non-empty line
        lines = content.strip().split("\n")
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if line:
                try:
                    tree = parser.parse(lexer.tokenize(line))
                    BasicExecute(tree, env)
                except Exception as e:
                    print(f"Error on line {line_num}: {e}")

        print("-" * 40)
        print("File execution completed.")

    except Exception as e:
        print(f"Error reading file '{filename}': {e}")


# Displaying the Program output
if __name__ == "__main__":
    lexer = BasicLexer()
    parser = BasicParser()

    # Check if a file argument was provided
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        execute_file(filename)
    else:
        # Interactive mode
        print(
            f"TC3002B Programming Language Program 1.0 (tags/v3.10.11, Jun 1 2025, 00:38:17)"
        )
        print(
            'Type "help", "credits",  or "exit" to exit the program.'
        )
        env = {}

        while True:
            try:
                text = input(">> ")
            except EOFError:
                break

            if text:
                if text.strip().lower() in ("exit", "quit"):
                    break
                elif text.strip().lower() == "help":
                    print(
                        "This is a simple interpreter for a basic programming language."
                    )
                    print(
                        "You can use variables, arithmetic operations, and if statements."
                    )
                    print("Type 'credits' to see the developers.")
                    print("Keywords: if, then, else, endif.")
                    print("Operators: +, -, *, /, <, >, =.")
                    print("Type 'exit' or 'quit' to exit the program.")
                    print("Type 'help' to see this message again.")
                    print("Type 'credits' to see the developers.")
                    print("Type 'file <filename>' to execute a file.")
                    print("Examples:")
                    print(">> x = 5")
                    print('>> y = "Hello"')
                    print(
                        '>> if x < 10 then y = "Less than 10" else y = "10 or more" endif'
                    )
                    print(">> y")
                    print('"Less than 10"')
                    print(
                        "In order to execute a file, run the program and then the <filename>'.")
                    print("For example: python CompilerProgram.py test.txt")
                    print("or: ./compiler test.txt")
                    continue
                elif text.strip().lower() == "credits":
                    print(
                        "Developed by Ivan Romero (A00833623) and Diego Hernandez (A00834015)."
                    )
                    print(
                        "Class TC3002B - Programming Language. Compiler Module by Dr. Kingsley Okoye.")
                    continue

                tree = parser.parse(lexer.tokenize(text))
                BasicExecute(tree, env)
