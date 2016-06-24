import sys
sys.path.append('..')

from semantic_parser.dependency import *
from progressbar import ProgressBar
import time

N = 100
texts = open('../genia_corpus').readlines()[:N]

PATH = '../stanford-corenlp-full-2015-12-09'
server = DependencyParserServer(PATH)
client = DependencyParserClient('localhost')

start = time.time()

server.start()
for text in ProgressBar()(texts):
    list(client.parse(text))
server.stop()

elapsed = time.time() - start
print('Parsed {} sentences in {:.2f} sec'.format(len(texts), elapsed))
print('{:.2f} sents/s'.format(len(texts)/elapsed))
