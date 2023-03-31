# (set-logic LIA)
# (synth-fun max ((x Int) (y Int)) Int
#   ((Start Int) (StartBool Bool))
#   ((Start Int (0 1 x y
#                (+ Start Start)
#                (- Start Start)
#                (ite StartBool Start Start)))
#    (StartBool Bool ((and StartBool StartBool)
#                     (not StartBool)
#                     (<= Start Start)))))
# (synth-fun min ((x Int) (y Int)) Int)
# (declare-var x Int)
# (declare-var y Int)
# (constraint (>= (max x y) x))
# (constraint (>= (max x y) y))
# (constraint (or (= x (max x y)) (= y (max x y))))
# (constraint (= (+ (max x y) (min x y)) (+ x y)))
# (check-synth)


from cvc5 import Kind
from synthesize.utils import synth_solutions, dump_smt, setup_solver
from interpret.smt_interpreter import interpret_smt, dump_python


if __name__ == "__main__":
    slv = setup_solver()

    integer = slv.getIntegerSort()
    boolean = slv.getBooleanSort()

    # declare input variables for the functions-to-synthesize
    x = slv.mkVar(integer, "x")
    y = slv.mkVar(integer, "y")

    # declare the grammar non-terminals
    start = slv.mkVar(integer, "Start")
    start_bool = slv.mkVar(boolean, "StartBool")

    # define the rules
    zero = slv.mkInteger(0)
    one = slv.mkInteger(1)

    plus = slv.mkTerm(Kind.ADD, start, start)
    minus = slv.mkTerm(Kind.SUB, start, start)
    ite = slv.mkTerm(Kind.ITE, start_bool, start, start)

    And = slv.mkTerm(Kind.AND, start_bool, start_bool)
    Not = slv.mkTerm(Kind.NOT, start_bool)
    leq = slv.mkTerm(Kind.LEQ, start, start)

    # create the grammar object
    g = slv.mkGrammar([x, y], [start, start_bool])

    # bind each non-terminal to its rules
    g.addRules(start, [zero, one, x, y, plus, minus, ite])
    g.addRules(start_bool, [And, Not, leq])

    # declare the functions-to-synthesize. Optionally, provide the grammar
    # constraints
    max = slv.synthFun("max", [x, y], integer, g)
    min = slv.synthFun("min", [x, y], integer)

    # declare universal variables.
    varX = slv.declareSygusVar("x", integer)
    varY = slv.declareSygusVar("y", integer)

    max_x_y = slv.mkTerm(Kind.APPLY_UF, max, varX, varY)
    min_x_y = slv.mkTerm(Kind.APPLY_UF, min, varX, varY)

    # add semantic constraints
    # (constraint (>= (max x y) x))
    slv.addSygusConstraint(slv.mkTerm(Kind.GEQ, max_x_y, varX))

    # (constraint (>= (max x y) y))
    slv.addSygusConstraint(slv.mkTerm(Kind.GEQ, max_x_y, varY))

    # (constraint (or (= x (max x y))
    #                 (= y (max x y))))
    slv.addSygusConstraint(slv.mkTerm(
        Kind.OR,
        slv.mkTerm(Kind.EQUAL, max_x_y, varX),
        slv.mkTerm(Kind.EQUAL, max_x_y, varY)))

    # (constraint (= (+ (max x y) (min x y))
    #                (+ x y)))
    slv.addSygusConstraint(slv.mkTerm(
        Kind.EQUAL,
        slv.mkTerm(Kind.ADD, max_x_y, min_x_y),
        slv.mkTerm(Kind.ADD, varX, varY)))

    if (slv.checkSynth().hasSolution()):
        terms = [max, min]
        smt_prog = synth_solutions(terms, slv.getSynthSolutions(terms))
        py_prog = interpret_smt(smt_prog)

        print(smt_prog)
        print(py_prog)

        dump_python("tests/py_output/test1.py", py_prog)
        dump_smt("tests/smt_output/test1.smt", smt_prog)
