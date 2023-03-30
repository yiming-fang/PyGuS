class Function():
    def __init__(self, tks):
        if tks:
            self.empty = False
            self.name = tks[2].value
            self.args = tks[4]
            self.typ  = tks[6]
            self.body = tks[7]
            self.f = tks[9]
        else:
            self.empty = True
    def eval(self):
        if self.empty:
            return ""
        this_fun =  "def " + self.name + self.args.eval() +\
                    " -> " + self.typ.eval() + ":\n\t" +\
                    self.body.eval()
        this_fun += self.f.eval()
        return this_fun

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

class Expr():
    def __init__(self, expr):
        self.expr = expr
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
        print(self.right.eval())
        return self.left.eval() + " " + str(self.op) + " " + self.right.eval()
        