from dataclasses import dataclass

class ImmutableMeta(type):
    def __new__(cls, name, bases, body, *args, **kwargs):
        assert "__iter__" not in body #todo msg
        anns = body.get("__annotations__", {})
        fields = [k for k in anns]
        def __iter__(self):
            for f in fields:
                yield getattr(self, f)
        new_body = {}
        new_body.update(body)
        new_body["__iter__"]  = __iter__
        c = type.__new__(cls, name, bases, new_body, *args, **kwargs)
        assert not any(x in kwargs for x in ["eq", "order", "unsafe_hash", "frozen", "match_args"])
        return dataclass(c, eq=True, order=True, unsafe_hash=False, frozen=True, match_args=True, **kwargs)

class Immutable(metaclass=ImmutableMeta): pass
