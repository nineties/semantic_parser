from nltk.parse.stanford import StanfordDependencyParser

class StanfordDP(object):
    def __init__(self, parser_path, models_path):
        self.parser_path = parser_path
        self.models_path = models_path
        self.parser = StanfordDependencyParser(
                path_to_jar=self.parser_path,
                path_to_models_jar=self.models_path
                )

    def parse(self, text):
        return self.parser.raw_parse(text).next()

    def parse_sents(self, texts):
        result = self.parser.raw_parse_sents(texts)
        for graph in result:
            yield graph.next().triples()
