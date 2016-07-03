import pandas as pd
import subprocess
import requests
import os

class DependencyParserServer(object):
    def __init__(self, corenlp_path, port=9000, timeout=5000):
        self.corenlp_path = corenlp_path
        self.port = port
        self.timeout = timeout
        self.proc = None

    def start(self):
        if self.proc:
            raise Exception('Double launch of dependency server.')

        DEVNULL = open(os.devnull, 'wb')

        self.proc = subprocess.Popen([
            'java', '-mx4g', '-cp', '{}/*'.format(self.corenlp_path),
            'edu.stanford.nlp.pipeline.StanfordCoreNLPServer',
            '-port', str(self.port),
            '-timeout', str(self.timeout)
            ],
            stdout=DEVNULL,
            stderr=subprocess.PIPE,
            bufsize=1
            )

        # Wait until the server is ready.
        for line in iter(self.proc.stderr.readline, ''):
            if line.find(b'StanfordCoreNLPServer listening') >= 0:
                break

        self.proc.stderr = DEVNULL
        return self.port

    def stop(self):
        if self.proc:
            self.proc.terminate()
            self.proc = None

    def __del__(self):
        if self.proc:
            self.proc.terminate()

class DependencyParserClient(object):
    def __init__(self, host, port=9000):
        self.host = host
        self.port = port

    def parse(self, text, remove_ROOT=True):
        params = {
            'annotators': 'parse',
            'outputFormat': 'json'
            }

        res = requests.post(
                'http://{}:{}'.format(self.host, self.port),
                data=text,
                params={'properties': repr(params)}
                )

        if res.status_code != 200:
            return

        data = res.json()

        # Convert JSON-object to panda's dataframes.
        for s in data['sentences']:
            df = pd.DataFrame.from_dict(s['tokens'])

            original_text = ' '.join(df['originalText'])
            tokens = df[['index', 'pos', 'word']]

            df = pd.DataFrame.from_dict(s['basic-dependencies'])
            deps = df[['dep', 'governor', 'dependent']]

            if remove_ROOT:
                deps = deps[deps['dep'] != 'ROOT']

            yield original_text, tokens, deps
