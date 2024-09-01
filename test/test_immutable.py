from dataclasses import field
import random
from unittest import TestCase

from test.random_util import random_other_than
from thinking_modules.immutable import Immutable

from lazy import lazy

class ImmutableTests(TestCase):
    def test_simple_immutable(self):
        class Simple(Immutable):
            a: int
            b: str
        x = Simple(1, "a")
        self.assertEqual(x.a, 1)
        self.assertEqual(x.b, "a")
        def set_a():
            x.a = 2
        def set_b():
            x.a = "2"
        self.assertRaises(Exception, set_a)
        self.assertRaises(Exception, set_b)

    def test_can_have_fields_with_defaults(self):
        random_val = None
        class NotThatSimple(Immutable):
            a: int = field(default=5)
            b: int = field(default_factory=lambda: random_val)

        random_val = random.randint(0, 0xDEADBEEF)
        x = NotThatSimple()
        self.assertEqual(x.a, 5)
        self.assertEqual(x.b, random_val)

        random_val = random.randint(0, 0xDEADBEEF)
        x = NotThatSimple(7)
        self.assertEqual(x.a, 7)
        self.assertEqual(x.b, random_val)

        random_val = random_other_than(10)
        x = NotThatSimple(9, 10)
        self.assertEqual(x.a, 9)
        self.assertEqual(x.b, 10)

        x = NotThatSimple(a=9, b=10)
        self.assertEqual(x.a, 9)
        self.assertEqual(x.b, 10)

        random_val = random_other_than(15)
        x = NotThatSimple(b=15, a=10)
        self.assertEqual(x.a, 10)
        self.assertEqual(x.b, 15)

    def test_allows_properties(self):
        class WithProp(Immutable):
            a: int
            b: str

            @property
            def c(self) -> tuple[str, int]:
                return (self.b, self.a)
        x = WithProp(1, "a")
        self.assertEqual(x.c, ("a", 1))

    def test_can_be_unpacked(self):
        def foo(x, y):
            self.assertEqual(x, 1)
            self.assertEqual(y, 2)
        class Tuplish(Immutable):
            a: int
            b: int
        foo(*Tuplish(1, 2))

    def test_allow_lazy_properties(self):
        cnt = 0
        class WithLazyProp(Immutable):
            a: int
            b: str

            @lazy
            def c(self) -> tuple[str, int]:
                nonlocal cnt
                cnt += 1
                return (self.b, self.a)
        x = WithLazyProp(1, "a")
        self.assertEqual(x.c, ("a", 1))
        self.assertEqual(cnt, 1)
        self.assertEqual(x.c, ("a", 1))
        self.assertEqual(cnt, 1)
