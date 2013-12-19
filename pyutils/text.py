import re

phone_re = r'1?\s*\W?\s*([2-9][0-8][0-9])\s*\W?\s*([2-9][0-9]{2})\s*\W?\s*([0-9]{4})(\se?x?t?(\d*))?'


_rd_txt1 = re.compile(r'(?:^[\s\W]+)|(?:[\s\W]+$)')
_rd_txt2 = re.compile(r'[^\w\d\s\-_]')
_rd_txt3 = re.compile(r'[\-\s\W]+')


def reduce_text(text, delimiter='_'):
    """
    Given arbitrary text (typically with spaces) and a delimiter, return
    a non-spaced term suitable as a label (e.g. for use as a CSS class).
    """
    text = _rd_txt1.sub('', text)
    text = _rd_txt2.sub('', text)
    return _rd_txt3.sub(delimiter, text).lower()


def plural(term, ct, include_count=True, preserve_singular=True):
    """
    Returns a string representation of a term's plural.
    """
    def suffix(term):
        return "es" if term.endswith(('ch', 'sh', 's', 'x')) else "s"

    result = "%i %s" % (ct, term) if include_count else term

    if preserve_singular:
        return result + (suffix(term) if ct != 1 else '')
    else:
        return result + (suffix(term))


def pluralize(term, ct):
    """
    Convenience function for simple pluralization.
    """
    return plural(term, ct, include_count=False, preserve_singular=False)


def smart_plural(clxn, singular, plural):
    return plural if len(clxn) > 1 else singular


def format_seq(seq):
    if not seq:
        return ""
    return seq[0] if len(seq) == 1 else " and ".join([", ".join(seq[0:-1]), seq[-1]])


def singularize(term):
    """Ghetto"""
    if term.endswith("s"):
        return term[:-1]


def format_seq(seq):
    """
    Given an arbitrary list of strings, join them into a compound phrase;
    return a single string if the list length is 1.
    """
    if not seq:
        return ""
    return seq[0] if len(seq) == 1 else " and ".join([", ".join(seq[0:-1]), seq[-1]])


def serialize_seq(seq):
    """
    Given an arbitrary list of strings, join them into a comma-separated list;
    return a single string if the list length is 1.
    """
    if not seq:
        return ""
    return seq[0] if len(seq) == 1 else ", ".join(seq)


def noreturns(text):
    return re.compile(r'[\r\n]').sub('', text)


def remove_tag(str_, tag="p"):
    tag_re = re.compile("(<%s>|<\/%s>)" % (tag, tag))
    return re.sub(tag_re, '', str_, re.M)


def camelize(text, initial_cap=True):
    text = initial_camelize(text)
    if text and initial_cap:
        text = text[0].upper() + text[1:]
    return text


def initial_camelize(text):
    def upcase(matchobj):
        return matchobj.group(0)[1:].upper()
    text = re.sub(r'(_[a-zA-Z])', upcase, text)
    if text:
        text = text[0].lower() + text[1:]
    return text


_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')
def uncamelize(s):
    subbed = _underscorer1.sub(r'\1_\2', s)
    return _underscorer2.sub(r'\1_\2', subbed).lower()


def underscores_as_words(text):
    def upcase(matchobj):
        return " " + matchobj.group(0)[1:].upper()
    text = re.sub(r'(_[a-zA-Z])', upcase, text)
    if text:
        text = text[0].upper() + text[1:]
    return text
