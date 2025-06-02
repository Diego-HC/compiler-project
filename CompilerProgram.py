# Building a Lexer - Tokenizer

from sly import Lexer, Parser


class BasicLexer(Lexer):
    tokens = {NAME, NUMBER, STRING, IF, THEN, ELSE, ENDIF}
    ignore = '\t '
    literals = {'=', '+', '-', '/',
                '*', '(', ')', ',', ';', '<', '>', '!'}

    # Define tokens as regular expressions

    # Keywords
    IF = r'if'
    THEN = r'then'
    ELSE = r'else'
    ENDIF = r'endif'

    # store as raw strings
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'

    # Number token
    @_(r'\d+')
    def NUMBER(self, t):
        # convert it into a python integer
        t.value = int(t.value)
        return t

    # Comment token
    @_(r'//.*')
    def COMMENT(self, t):
        pass

    # Newline token(used only for showing errors in new line)
    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')


class BasicParser(Parser):
    # tokens are passed from lexer to parser
    tokens = BasicLexer.tokens

    precedence = (
        ('left', 'EQUALS_TO'),
        ('left', '<', '>'),
        ('left', 'IF', 'THEN', 'ELSE', 'ENDIF'),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = {}

    @_('')
    def statement(self, p):
        pass

    @_('if_stmt')
    def statement(self, p):
        return p.if_stmt

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('NAME "=" STRING')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('expr "<" expr')
    def expr(self, p):
        return ('lt', p.expr0, p.expr1)

    @_('expr ">" expr')
    def expr(self, p):
        return ('gt', p.expr0, p.expr1)

    @_('IF expr THEN statement ENDIF')
    def if_stmt(self, p):
        return ('if', p.expr, p.statement, None)

    @_('IF expr THEN statement ELSE statement ENDIF')
    def if_stmt(self, p):
        return ('if', p.expr, p.statement0, p.statement1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)


class BasicExecute:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])

        if node[0] == 'lt':
            return self.walkTree(node[1]) < self.walkTree(node[2])
        elif node[0] == 'gt':
            return self.walkTree(node[1]) > self.walkTree(node[2])

        if node[0] == 'if':
            condition = self.walkTree(node[1])
            print("Condition evaluated to:", condition)
            print("node", node)
            if condition:
                return self.walkTree(node[2])  # then branch
            elif node[3] is not None:
                return self.walkTree(node[3])  # else branch

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return 0


# Displaying the Program output
if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    print('TC3002B Programming Language Program 1.0 (tags/v3.10.11:7d4cc5a, Jun 1 2025, 00:38:17')
    print('TC3002B Programming Language Program')
    print('A00833623 - Ivan Romero')
    print('A00834015 - Diego Hernandez')
    env = {}

    while True:

        try:
            text = input('Make input to Program here> ')

        except EOFError:
            break

        if text:
            tree = parser.parse(lexer.tokenize(text))
            BasicExecute(tree, env)
