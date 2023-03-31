from rply import ParserGenerator
from interpret.smt_ast import Value, BinOp, UOp, Function, Args, Cond

class Parser():
    def __init__(self):
        self.tks = ['FUN', 'NUM', 'VAR']
        self.prs = ['LP', 'RP']
        self.ops = ['ADD', 'SUB', 'MUL', 'DIV', 
                    'AND', 'OR', 
                    'EQ', 'LEQ', 'GEQ',
                    'NOT', 'ITE']
        self.tys = ['INT', 'BOOL']
        
        self.pg = ParserGenerator(
            self.tks + self.prs + self.ops + self.tys
        )

    def parse(self):
        @self.pg.production('''function :   LP 
                                                FUN VAR LP args RP type expr 
                                            RP 
                                            function''')
        @self.pg.production('''function : ''')
        def function(tks):
            return Function(tks)

        @self.pg.production('args : LP VAR type RP args')
        @self.pg.production('args : ')
        def args(tks):
            return Args(tks)

        @self.pg.production('type : INT')
        @self.pg.production('type : BOOL')
        def type(tks):
            return Value(tks[0].value.lower())

        @self.pg.production('expr : LP ADD expr expr RP')
        @self.pg.production('expr : LP SUB expr expr RP')
        @self.pg.production('expr : LP MUL expr expr RP')
        @self.pg.production('expr : LP DIV expr expr RP')
        @self.pg.production('expr : LP AND expr expr RP')
        @self.pg.production('expr : LP OR  expr expr RP')
        @self.pg.production('expr : LP EQ  expr expr RP')
        @self.pg.production('expr : LP LEQ expr expr RP')
        @self.pg.production('expr : LP GEQ expr expr RP')
        def binop(tks):
            return BinOp(tks[1], tks[2], tks[3])

        @self.pg.production('expr : LP SUB expr RP')
        @self.pg.production('expr : LP NOT expr RP')
        def uop(tks):
            return UOp(tks[1], tks[2])

        @self.pg.production('expr : LP ITE expr expr expr RP')
        def conditional(tks):
            return Cond(tks[2], tks[3], tks[4])

        @self.pg.production('expr : NUM')
        @self.pg.production('expr : VAR')
        def value(tks):
            return Value(tks[0].value)

        @self.pg.error
        def error_handle(tks):
            raise ValueError(tks)

    def get_parser(self):
        return self.pg.build()
