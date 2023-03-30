from rply import ParserGenerator
from smt_ast import Expr, Value, BinOp, Function, Args

class Parser():
    def __init__(self):
        self.tks = ['FUN', 'NUM', 'VAR']
        self.prs = ['LPAREN', 'RPAREN']
        self.ops = ['ADD', 'SUB', 'MUL', 'DIV', 
                    'AND', 'OR', 
                    'EQ', 'LEQ', 'GEQ']
                    #'NOT', 'ITE', 'NEG']
        self.tys = ['INT', 'BOOL']
        
        self.pg = ParserGenerator(
            self.tks + self.prs + self.ops + self.tys
        )

    def parse(self):
        @self.pg.production('''function :   LPAREN 
                                                FUN VAR LPAREN args RPAREN type expr 
                                            RPAREN 
                                            function''')
        @self.pg.production('''function : ''')
        def function(tks):
            return Function(tks)

        @self.pg.production('args : LPAREN VAR type RPAREN args')
        @self.pg.production('args : ')
        def args(tks):
            return Args(tks)

        @self.pg.production('type : INT')
        @self.pg.production('type : BOOL')
        def type(tks):
            return Value(tks[0].value)

        @self.pg.production('expr : LPAREN expr RPAREN')
        def expr(tks):
            return Expr(tks[1])

        @self.pg.production('expr : ADD expr expr')
        @self.pg.production('expr : SUB expr expr')
        @self.pg.production('expr : MUL expr expr')
        @self.pg.production('expr : DIV expr expr')
        @self.pg.production('expr : AND expr expr')
        @self.pg.production('expr : OR expr expr')
        @self.pg.production('expr : EQ expr expr')
        @self.pg.production('expr : LEQ expr expr')
        @self.pg.production('expr : GEQ expr expr')
        def binop(tks):
            for t in tks:
                print(t)
            return BinOp(tks[0], tks[1], tks[2])

        @self.pg.production('expr : NUM')
        @self.pg.production('expr : VAR')
        def value(tks):
            return Value(tks[0].value)

        @self.pg.error
        def error_handle(tks):
            raise ValueError(tks)

    def get_parser(self):
        return self.pg.build()
