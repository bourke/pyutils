from __future__ import print_function
from __future__ import absolute_import

VERSION = (0, 4, 0)
DEV_STATUS = '4 - Beta'

from .text import *
# (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

try:
    from itertools import izip as zip, izip_longest as zip_longest, tee
except ImportError:
    from itertools import zip_longest, tee


import collections
from functools import wraps


def walkable(obj):
    return (isinstance(obj, collections.Iterable)
        and not isinstance(obj, basestring))


def walk_object(obj, f=(lambda x: x)):
    # print obj, type(obj), walkable(obj)
    if not walkable(obj):
        # print "call func with %s (%s)?" % (obj, type(obj))
        obj = f(obj)
    else:
        if isinstance(obj, collections.Mapping):
            it = obj.itervalues()
        else:
            it = iter(obj)
        for obj in it:
            walk_object(obj, f)
    return obj


class hybridmethod(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        context = obj if obj is not None else cls

        @wraps(self.func)
        def hybrid(*args, **kw):
            return self.func(context, *args, **kw)

        # optional, mimic methods some more
        hybrid.__func__ = hybrid.im_func = self.func
        hybrid.__self__ = hybrid.im_self = context

        return hybrid


class classproperty(property):
    """A decorator that behaves like @property except that operates
    on classes rather than instances.

    """
    def __get__(desc, self, cls):
        return desc.fget(cls)


def pluck(obj, *keys):
    rv = {}
    for k in keys:
        try:
            rv.update({k: obj.get(k)})
        except:
            continue
    return rv


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


def group_seq(iterable, n, fill=True, fillvalue=None):
    """Group a sequence into <n> subsequences:
       grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    """
    args = [iter(iterable)] * n
    if fill:
        return zip_longest(fillvalue=fillvalue, *args)
    else:
        return zip(*args)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) \
                and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el


class OrderedDefaultdict(collections.OrderedDict):
    def __init__(self, *args, **kwargs):
        if not args:
            self.default_factory = None
        else:
            if not (args[0] is None or callable(args[0])):
                raise TypeError('first argument must be callable or None')
            self.default_factory = args[0]
            args = args[1:]
        super(OrderedDefaultdict, self).__init__(*args, **kwargs)

    def __missing__ (self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = default = self.default_factory()
        return default

    def __reduce__(self):  # optional, for pickle support
        args = (self.default_factory,) if self.default_factory else ()
        return self.__class__, args, None, None, self.iteritems()

