# (set-logic LIA)
# (synth-fun id1 ((x Int)) Int ((Start Int)) ((Start Int ((- x) (+ x Start)))))
# (synth-fun id2 ((x Int)) Int ((Start Int)) ((Start Int ((Variable Int) (- x) (+ x Start)))))
# (synth-fun id3 ((x Int)) Int ((Start Int)) ((Start Int (0 (- x) (+ x Start)))))
# (synth-fun id4 ((x Int)) Int ((Start Int)) ((Start Int ((- x) (+ x Start)))))
# (declare-var x Int)
# (constraint (= (id1 x) (id2 x) (id3 x) (id4 x) x))
# (check-synth)


from cvc5 import Kind
from synthesize.utils import synth_solutions, dump_smt, setup_solver
from interpret.smt_interpreter import interpret_smt, dump_python


if __name__ == "__main__":
    slv = setup_solver()

    integer = slv.getIntegerSort()

    # declare input variable for the function-to-synthesize
    x = slv.mkVar(integer, "x")

    # declare the grammar non-terminal
    start = slv.mkVar(integer, "Start")

    # define the rules
    zero = slv.mkInteger(0)
    neg_x = slv.mkTerm(Kind.NEG, x)
    plus = slv.mkTerm(Kind.ADD, x, start)

    # create the grammar object
    g1 = slv.mkGrammar([x], [start])
    g2 = slv.mkGrammar([x], [start])
    g3 = slv.mkGrammar([x], [start])

    # bind each non-terminal to its rules
    g1.addRules(start, [neg_x, plus])
    g2.addRules(start, [neg_x, plus])
    g3.addRules(start, [neg_x, plus])

    # add parameters as rules for the start symbol. Similar to "(Variable Int)"
    g2.addAnyVariable(start)

    # declare the functions-to-synthesize
    id1 = slv.synthFun("id1", [x], integer, g1)
    id2 = slv.synthFun("id2", [x], integer, g2)

    g3.addRule(start, zero)

    id3 = slv.synthFun("id3", [x], integer, g3)

    # g1 is reusable as long as it remains unmodified after first use
    id4 = slv.synthFun("id4", [x], integer, g1)

    # declare universal variables.
    varX = slv.declareSygusVar("x", integer)

    id1_x = slv.mkTerm(Kind.APPLY_UF, id1, varX)
    id2_x = slv.mkTerm(Kind.APPLY_UF, id2, varX)
    id3_x = slv.mkTerm(Kind.APPLY_UF, id3, varX)
    id4_x = slv.mkTerm(Kind.APPLY_UF, id4, varX)

    # add semantic constraints
    # (constraint (= (id1 x) (id2 x) (id3 x) (id4 x) x))
    slv.addSygusConstraint(
        slv.mkTerm(Kind.AND,
                   slv.mkTerm(Kind.EQUAL, id1_x, id2_x),
                   slv.mkTerm(Kind.EQUAL, id1_x, id3_x),
                   slv.mkTerm(Kind.EQUAL, id1_x, id4_x),
                   slv.mkTerm(Kind.EQUAL, id1_x, varX)))

    if (slv.checkSynth().hasSolution()):
        terms = [id1, id2, id3, id4]
        smt_prog = synth_solutions(terms, slv.getSynthSolutions(terms))
        py_prog = interpret_smt(smt_prog)

        print(smt_prog)
        print(py_prog)

        dump_python("tests/py_output/test2.py", py_prog)
        dump_smt("tests/smt_output/test2.smt", smt_prog)
