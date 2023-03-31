# (set-logic LIA)
# (synth-inv inv_f ((x Int)))
# (define_fun pre_f ((x Int)) Bool (= x 0))
# (define_fun trans_f ((x Int) (xp Int)) Bool (ite (< x 10) (= xp (+ x 1)) (= xp x)))
# (define_fun post_f ((x Int)) Bool (<= x 10))
# (inv-constraint inv_f pre_f trans_f post_f)
# (check-synth)


from cvc5 import Kind, Solver
from synthesize.utils import synth_solutions, dump_smt, setup_solver
from interpret.smt_interpreter import interpret_smt, dump_python

if __name__ == "__main__":
    slv = setup_solver()

    integer = slv.getIntegerSort()
    boolean = slv.getBooleanSort()

    zero = slv.mkInteger(0)
    one = slv.mkInteger(1)
    ten = slv.mkInteger(10)

    # declare input variables for functions
    x = slv.mkVar(integer, "x")
    xp = slv.mkVar(integer, "xp")

    # (ite (< x 10) (= xp (+ x 1)) (= xp x))
    ite = slv.mkTerm(Kind.ITE,
                     slv.mkTerm(Kind.LT, x, ten),
                     slv.mkTerm(Kind.EQUAL, xp, slv.mkTerm(Kind.ADD, x, one)),
                     slv.mkTerm(Kind.EQUAL, xp, x))

    # define the pre-conditions, transition relations, and post-conditions
    pre_f = slv.defineFun("pre_f", [x], boolean,
                          slv.mkTerm(Kind.EQUAL, x, zero))
    trans_f = slv.defineFun("trans_f", [x, xp], boolean, ite)
    post_f = slv.defineFun(
        "post_f", [x], boolean, slv.mkTerm(Kind.LEQ, x, ten))

    # declare the invariant-to-synthesize
    inv_f = slv.synthInv("inv_f", [x])

    slv.addSygusInvConstraint(inv_f, pre_f, trans_f, post_f)

    # print solutions if available
    if slv.checkSynth().hasSolution():
        terms = [inv_f]
        smt_prog = synth_solutions(terms, slv.getSynthSolutions(terms))
        py_prog = interpret_smt(smt_prog)

        print(smt_prog)
        print(py_prog)

        dump_python("tests/py_output/test3.py", py_prog)
        dump_smt("tests/smt_output/test3.smt", smt_prog)
