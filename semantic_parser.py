from collections import namedtuple

Const = namedtuple('Const', 'id')
Var = namedtuple('Var', 'id')
Atom = namedtuple('Atom', 'pred arg')
Rel = namedtuple('Rel', 'pred lhs rhs')

class SkolemTranslator(object):
    def __init__(self):
        self.atoms = {}
        self.id = 0

    def skolem_var(self, node):
        if node in self.atoms:
            return self.atoms[node].arg

        c = Const(self.id)
        self.atoms[node] = Atom(pred=node, arg=c)

        self.id += 1
        return c

# Convert a dependency triples to a QLF(quasi-logical form)
def convert_from_triples(triples):
    transl = SkolemTranslator()
    formulas = []

    for x, rel, y in triples:
        x = transl.skolem_var(x)
        y = transl.skolem_var(y)
        formulas.append(Rel(pred=rel, lhs=x, rhs=y))

    formulas.extend(transl.atoms.values())
    return formulas
