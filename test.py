from stanforddp import StanfordDP

dp = StanfordDP(
    'stanford-corenlp-full-2015-04-20/stanford-corenlp-3.5.2.jar',
    'stanford-corenlp-full-2015-04-20/stanford-corenlp-3.5.2-models.jar'
    )

for ts in dp.parse_sents(['Utah borders Idaho.', 'I am Koichi.']):
    for t in ts:
        print t
