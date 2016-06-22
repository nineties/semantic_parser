import subprocess

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
            stderr=subprocess.DEVNULL
            )

    def stop(self):
        if self.proc:
            self.proc.terminate()
            self.proc = None

    def __del__(self):
        if self.proc:
            self.proc.terminate()
