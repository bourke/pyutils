VERSION = (0, 2, 0)
DEV_STATUS = '4 - Beta'

from text import *
# (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

from itertools import izip_longest
import collections


def last_iteritem(it):
    d = collections.deque(it, maxlen=1)
    return d.pop()


def asbool(obj):
    if isinstance(obj, (str, unicode)):
        obj = obj.strip().lower()
        if obj in ['true', 'yes', 'on', 'y', 't', '1']:
            return True
        elif obj in ['false', 'no', 'off', 'n', 'f', '0']:
            return False
        else:
            raise ValueError(
                "String is not true/false: %r" % obj)
    return bool(obj)


def aslist(obj, sep=None, strip=True):
    if isinstance(obj, (str, unicode)):
        lst = obj.split(sep)
        if strip:
            lst = [v.strip() for v in lst]
        return lst
    elif isinstance(obj, (list, tuple)):
        return obj
    elif obj is None:
        return []
    else:
        return [obj]


def to_list(x, default=None):
    if x is None:
        return default
    if not isinstance(x, (list, tuple)):
        return [x]
    else:
        return list(x)


def iter_islast(iterable):
    """ iter_islast(iterable) -> generates (item, islast) pairs

    Generates pairs where the first element is an item from the iterable
    source and the second element is a boolean flag indicating if it is the
    last item in the sequence.
    """
    it = iter(iterable)
    prev = it.next()
    for item in it:
        yield prev, False
        prev = item
    yield prev, True


def iter_isfirst(iterable):
    """iter_isfirst(iterable) -> generates (item, isfirst) pairs
    Generates pairs of x, y where x is the item from the iterable source and y is
    a boolean indicating whether it is the first in the sequence.
    """
    it = iter(iterable)
    yield it.next(), True
    for item in it:
        yield item, False


def divide_seq(seq, divisor):
    """Divide a sequence into <divisor> subsequences"""
    if not seq:
        return []
    t = seq
    stop = len(t) / divisor + (1 if len(t) % divisor else 0)
    return [[i for i in t[0 + j:stop + j]] for j in range(0, len(t), stop)]


def group_seq(iterable, n, fillvalue=None):
    """Group a sequence into <n> subsequences:
       grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    """
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) \
                and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

