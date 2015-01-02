import contextlib
import sys

from chardet.universaldetector import UniversalDetector

def detect_encoding(data):
    u = UniversalDetector()
    for line in data.splitlines():
        print line
        u.feed(line)
        if u.done:
            break
    u.close()
    return u.result['encoding'].lower()

@contextlib.contextmanager
def sysencoding(new_enc):
    reload(sys)
    old_enc = sys.getdefaultencoding()
    sys.setdefaultencoding(new_enc)
    yield
    sys.setdefaultencoding(old_enc)