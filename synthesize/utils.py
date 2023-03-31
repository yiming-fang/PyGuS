from cvc5 import Solver, Kind


def define_fun_to_string(f, params, body):
    sort = f.getSort()
    if sort.isFunction():
        sort = f.getSort().getFunctionCodomainSort()
    result = "(define-fun " + str(f) + " ("
    for i in range(0, len(params)):
        if i > 0:
            result += " "
        result += "(" + str(params[i]) + " " + str(params[i].getSort()) + ")"
    result += ") " + str(sort) + " " + str(body) + ")"
    return result


def synth_solutions(terms, sols):
    result = ""
    for i in range(0, len(terms)):
        params = []
        body = None
        if sols[i].getKind() == Kind.LAMBDA:
            params += sols[i][0]
            body = sols[i][1]
        result += define_fun_to_string(terms[i], params, body) + "\n"
    return result


def setup_solver():
    slv = Solver()
    slv.setOption("sygus", "true")
    slv.setOption("incremental", "false")
    slv.setLogic("LIA")
    return slv


def dump_smt(path, prog):
    f = open(path, "w+")
    f.write(prog)
    f.close()
