from semantic_parser import SemanticParser

# Load training data. List of sentences.
corpus = open('genia_corpus').read().strip().split('\n')

# Stanford CoreNLP (Download it from http://stanfordnlp.github.io/CoreNLP)
DEP_PARSER = 'stanford-corenlp-full-2015-04-20/stanford-corenlp-3.5.2.jar'
DEP_MODELS = 'stanford-corenlp-full-2015-04-20/stanford-corenlp-3.5.2-models.jar'

parser = SemanticParser(
        dep_parser=DEP_PARSER,
        dep_models=DEP_MODELS
        )

parser.train(corpus)

#dp = StanfordDP(
#    )
#
#result = dp.parse('I saw the book which I bought.')
##result = dp.parse('Utah borders Idaho.')
#
#print result.tree()
#print list(result.triples())
#print semantic_parser.convert_from_triples(result.triples())
