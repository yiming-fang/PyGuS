class Function():
    def __init__(self, tks):
        if tks:
            self.empty = False
            self.name = tks[2].value
            self.args = tks[4]
            self.typ  = tks[6]
            self.body = tks[7]
            self.next_funs = tks[9]
        else:
            self.empty = True

    def eval(self):
        if self.empty:
            return ""
        fun_string =  "def " + self.name + self.args.eval() +\
                      " -> " + self.typ.eval() + ":\n\t" +\
                      self.body.eval()
        return fun_string + self.next_funs.eval()

class Args():
    def __init__(self, tks):
        if tks:
            self.empty = False
            self.var = tks[1].value
            self.typ = tks[2]
            self.args = tks[4]
        else:
            self.empty = True
        
    def eval(self):
        if self.empty:
            return ""
        return "(" + self.var + ": " + self.typ.eval() + self.args.eval() + ")"


def parens(string):
    return "(" + string + ")"

class Expr():
    def __init__(self, expr):
        self.expr = expr
        self.str = ""

    def eval(self):
        return self.expr.eval()

class Value():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return str(self.value)

class BinOp(Expr):
    def __init__(self, op, left, right):
        self.left = left
        self.right = right
        self.op = op.value

    def eval(self):
        self.str = self.left.eval() + " " + str(self.op) + " " + self.right.eval()
        return parens(self.str)

class UOp(Expr):
    def __init__(self, operator, oprand):
        self.operand = oprand
        self.operator = operator.value
        
    def eval(self):
        self.str = str(self.operator) + " " + self.operand.eval()
        return parens(self.str)

class Cond(Expr):
    def __init__(self, if_clause, then_clause, else_clause):
        self.if_clause = if_clause
        self.then_clause = then_clause
        self.else_clause = else_clause

    def eval(self):
        self.str = self.then_clause.eval() + " if " +\
                   self.if_clause.eval() + " else " +\
                   self.else_clause.eval()
        return parens(self.str)
        