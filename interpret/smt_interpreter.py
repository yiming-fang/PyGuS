from interpret.smt_lexer import Lexer
from interpret.smt_parser import Parser


def interpret_smt(smt_prog: str) -> str:
    lexer = Lexer().get_lexer()
    tokens = lexer.lex(smt_prog)

    pg = Parser()
    pg.parse()
    parser = pg.get_parser()
    python_prog = parser.parse(tokens).eval()

    return python_prog


def dump_python(path, prog):
    f = open(path, "a")
    f.write(prog)
    f.close()
