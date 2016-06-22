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
