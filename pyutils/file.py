import contextlib
import codecs
import sys

@contextlib.contextmanager
def open_or_stdout(filename=None):
    if filename and filename != '-':
        fh = codecs.open(filename, 'w', encoding='utf-8')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

