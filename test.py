from stanforddp import StanfordDP
import semantic_parser

dp = StanfordDP(
    'stanford-corenlp-full-2015-04-20/stanford-corenlp-3.5.2.jar',
    'stanford-corenlp-full-2015-04-20/stanford-corenlp-3.5.2-models.jar'
    )

result = dp.parse('I saw the book which I bought.')
#result = dp.parse('Utah borders Idaho.')

print result.tree()
print list(result.triples())
print semantic_parser.convert_from_triples(result.triples())
