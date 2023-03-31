from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Keywords
        self.lexer.add('FUN', r'define-fun')

        # Parenthesis
        self.lexer.add('LP', r'\(')
        self.lexer.add('RP', r'\)')

        # Ops
        self.lexer.add('NOT', r'not')

        self.lexer.add('ADD', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')
        self.lexer.add('AND', r'and')
        self.lexer.add('OR', r'or')
        self.lexer.add('EQ', r'\=')
        self.lexer.add('GEQ', r'\>\=')
        self.lexer.add('LEQ', r'\<\=')

        self.lexer.add('ITE', r'ite')

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
