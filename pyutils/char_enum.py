"""Basic enum type that supports database persistence using a character value.

e.g.::

    class MaritalStatus(CharEnum):
        married = 'M', "married"
        single = 'S', "single"

    class User(Base):
        __tablename__ = 'user'

        martial_status = Column(CharEnumType(MaritalStatus))

"""
__all__ = ['CharEnum', 'sym']

import re

from functools import total_ordering


@total_ordering
class sym(object):
    def __init__(self, cls_, value, name, description, sort_order=None):
        self.cls_ = cls_
        self.value = value
        self.name = name
        self.description = description
        self.sort_order = sort_order

    def __reduce__(self):
        """establish the symbol's identity as a singleton
        when deserialized."""

        return getattr, (self.cls_, self.name)

    # TODO: better ?  or inconsistent?
    #def __str__(self):
    #    return self.description or self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "char_enum.sym(%r)" % self.name

    def __lt__(self, other):
        if self.sort_order and other.sort_order:
            return self.sort_order < other.sort_order
        else:
            return self.name < other.name

    def __eq__(self, other):
        return self is other


class CharMeta(type):
    def __init__(cls, classname, bases, dict_):
        if classname != 'CharEnum':
            if hasattr(cls, '_reg'):
                cls._reg = reg = cls._reg.copy()
            else:
                cls._reg = reg = {}
            for k, v in dict_.iteritems():
                if isinstance(v, (basestring, tuple)) and k[0] != '_':
                    if isinstance(v, tuple):
                        if len(v) == 2:
                            v, description = v
                            sort_order = None
                        elif len(v) == 3:
                            v, description, sort_order = v
                        else:
                            raise ValueError("Invalid tuple for %r: %r" % (cls, v))
                    else:
                        # MB:
                        # default ".description" to the "name" field -no ?
                        description = k
                        sort_order = None
                    v = sym(cls, v, k, description, sort_order)
                    dict_[k] = v
                    setattr(cls, k, v)
                    reg[v.value] = v
        return type.__init__(cls, classname, bases, dict_)

    def __setattr__(cls, key, value):
        if isinstance(value, (basestring, tuple)) and key[0] != '_':
            if isinstance(value, tuple):
                if len(value) == 2:
                    value, description = value
                    sort_order = None
                elif len(value) == 3:
                    value, description, sort_order = value
                else:
                    raise ValueError("Invalid tuple for %r: %r" % (cls, value))
            else:
                description = None
                sort_order = None
            value = sym(cls, value, key, description, sort_order)
            cls._reg[value.value] = value
        type.__setattr__(cls, key, value)


class CharEnum(object):
    __metaclass__ = CharMeta

    _coerce_from_str = re.compile(r'[\s-]')

    @classmethod
    def resolve(cls, value):
        try:
            return cls.from_string(value)
        except ValueError:
            return cls.coerce_from_string(value)

    @classmethod
    def from_string(cls, str_):
        try:
            return cls._reg[str_]
        except KeyError:
            raise ValueError("Invalid value for %r: %r" % (cls, str_))

    @classmethod
    def coerce_from_string(cls, value):
        if isinstance(value, basestring):
            return cls.__dict__[cls._coerce_from_str.sub('_', value.lower())]
        else:
            return value

    @classmethod
    def values(cls):
        return cls._reg.keys()

    @classmethod
    def symbols(cls):
        if cls._reg.values()[0].sort_order is not None:
            return sorted(cls._reg.values(), key=lambda s: s.sort_order)
        else:
            return sorted(cls._reg.values(), key=lambda s: s.name)


