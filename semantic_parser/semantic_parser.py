from .dependency import DependencyParserClient

class QuasiLogicalForm(object):
    def __init__(self, original_text, words, deps):
        self.original_text = original_text
        self.words = words
        self.deps = deps

    def __str__(self):
        print(self.words)
        print(self.deps)
        uni = [
            u'{}(a{})'.format(r['word'], r['index'])
            for i, r in self.words.iterrows()
            ]
        bin = [
            u'{}(a{},a{})'.format(r['dep'], r['lhs'], r['rhs'])
            for i, r in self.deps.iterrows()
            if i != 0
        ]
        return '&'.join(uni+bin)

class SemanticParser(object):
    def __init__(self, dpserver):
        self.dpcli = DependencyParserClient(*dpserver)

    def train(self, corpus):
        for text in corpus:
            for tree in self.dpcli.parse(text):
                print(QuasiLogicalForm(*tree))
