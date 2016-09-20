from poplib import POP3, error_proto
import glob

class FakePOP3(POP3):

    username = 'test'
    password = 'test'
    files = []

    def __init__(self, hostname, port=110):
        self.hostname = hostname
        self.port = port

        # Load files from tests/data directory
        for file in glob.glob("tests/data/*.eml"):
            self.files.append(file)

    def stat(self):
        return (len(self.files), 0,)

    def getwelcome(self):
        return "Welcome to fake account"

    def user(self, user):
        if user != self.username:
            raise error_proto("Wrong username.")

    def pass_(self, pswd):
        if pswd != self.password:
            raise error_proto("Wrong password.")

    def list(self, which=None):
        # eg. ('+OK 4 messages:', ['1 71017', '2 2201', '3 7723', '4 44152'], 34)
        files = self.files
        responses = []
        for i, f in enumerate(files):
            responses.append('%s %s' % (i+1, os.stat(f)[stat.ST_SIZE]))
        return ('+OK %s messages:' % len(files), responses, None)

    def top(self, which, size):
        return self.retr(which)

    def retr(self, which):
        # ['response', ['line', ...], octets]
        filename = self.files[which-1]
        content = [x.rstrip() for x in open(filename, 'rU').xreadlines()]
        return ('response', content, None)

    def quit(self):
        pass