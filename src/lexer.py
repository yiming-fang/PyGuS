from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Keywords
        self.lexer.add('FUN', r'define-fun')

        # Parenthesis
        self.lexer.add('LPAREN', r'\(')
        self.lexer.add('RPAREN', r'\)')

        # Unary Ops
        self.lexer.add('NOT', r'not')

        # Binary Ops
        self.lexer.add('ADD', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')

        self.lexer.add('EQ', r'\=')
        self.lexer.add('GEQ', r'\>\=')
        self.lexer.add('LEQ', r'\<\=')

        # Ternery Ops
        self.lexer.add('LEQ', r'ite')

        # Number
        self.lexer.add('NUM', r'\d+')

        # Variables
        self.lexer.add('VAR', r'[a-z\d*\_*\-*]+')

        # Types
        self.lexer.add('INT', r'Int')
        self.lexer.add('BOOL', r'Bool')

        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
