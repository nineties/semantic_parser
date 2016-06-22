import pandas as pd
import subprocess
import requests

class DependencyParserServer(object):
    def __init__(self, corenlp_path, port=9000, timeout=5000):
        self.corenlp_path = corenlp_path
        self.port = port
        self.timeout = timeout
        self.proc = None

    def start(self):
        if self.proc:
            raise Exception('Double launch of dependency server.')

        self.proc = subprocess.Popen([
            'java', '-mx4g', '-cp', '{}/*'.format(self.corenlp_path),
            'edu.stanford.nlp.pipeline.StanfordCoreNLPServer',
            '-port', str(self.port),
            '-timeout', str(self.timeout)
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            bufsize=1
            )

        # Wait until the server is ready.
        for line in iter(self.proc.stderr.readline, ''):
            if line.find(b'StanfordCoreNLPServer listening') >= 0:
                break

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

    def parse(self, text):
        params = {
            'annotators': 'parse',
            'outputFormat': 'json'
            }

        data = requests.post(
                'http://{}:{}'.format(self.host, self.port),
                data=text,
                params={'properties': repr(params)}
                ).json()

        # Convert JSON-object to panda's dataframes.
        for s in data['sentences']:
            df = pd.DataFrame.from_dict(s['tokens'])

            original_text = ' '.join(df['originalText'])
            tokens = df[['index', 'pos', 'word']]

            df = pd.DataFrame.from_dict(s['basic-dependencies'])
            print(df)
            deps = df[['dep', 'governor', 'dependent']]
            deps.columns = ['dep', 'lhs', 'rhs']

            yield original_text, tokens, deps
