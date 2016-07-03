import pandas as pd
from .dependency import DependencyParserClient

class QuasiLogicalForm(object):
    def __init__(self, original_text, words, deps):
        self.original_text = original_text
        self.words = words
        self.deps = deps

    def __str__(self):
        uni = [
            u'{}(a{})'.format(r['word'], r['index'])
            for i, r in self.words.iterrows()
            ]
        bin = [
            u'{}(a{},a{})'.format(r['dep'], r['governor'], r['dependent'])
            for i, r in self.deps.iterrows()
            if r['dep'] != 'ROOT'
        ]
        return '&'.join(uni+bin)

class SemanticParser(object):
    def __init__(self, dpserver):
        self.dpcli = DependencyParserClient(*dpserver)

    def preprocess(self, corpus):
        return [
            QuasiLogicalForm(*tree)
            for text in corpus
            for tree in self.dpcli.parse(text)
            ]

    def train(self, corpus, preprocess=True):
        qlfs = self.preprocess(corpus) if preprocess else corpus
        core_forms, arg_forms = self._create_initials(qlfs)

    def _create_initials(self, qlfs):
        # Re-index core forms so that they become unique.
        offset = 0
        for qlf in qlfs:
            qlf.words.index += offset
            qlf.deps['governor'] += offset
            qlf.deps['dependent'] += offset
            offset += len(qlf.words)

        # Combine all tables.
        core_forms = pd.concat(qlf.words for qlf in qlfs)
        arg_forms = pd.concat(qlf.deps for qlf in qlfs)

        # Create initial parts and clusters for each core forms.
        core_forms['part'] = range(len(core_forms))
        core_forms['cluster'] = range(len(core_forms))

        # Assign arg forms to the initial parts.
        arg_forms = pd.merge(arg_forms, core_forms[['part']],
                left_on='governor', right_index=True)

        # Create initial argtypes for each arg forms.
        arg_forms['type'] = range(len(arg_forms))

        return core_forms, arg_forms
