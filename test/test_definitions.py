from unittest import TestCase

from test.fixtures import AClass
from thinking_modules.definitions import type_, instance
from thinking_modules.model import ModuleName


class instanceTest(TestCase):
    def test_type_defined_in(self):
        t = type_(AClass)
        self.assertEqual(t.defining_module, ModuleName.of("test.fixtures"))

    def test_instance_defined_in(self):
        i = instance(AClass())
        self.assertEqual(i.type_.defining_module, ModuleName.of("test.fixtures"))
    def test_type_checks_w_module_name(self):
        t = type_(AClass)
        self.assertTrue(t.defined_in_module(ModuleName.of("test.fixtures")))
        self.assertTrue(t.defined_in_package(ModuleName.of("test.fixtures")))
        self.assertTrue(t.defined_in_package(ModuleName.of("test")))
        self.assertFalse(t.defined_in_module(ModuleName.of("test.subpackage")))
        self.assertFalse(t.defined_in_package(ModuleName.of("test.subpackage")))
        self.assertFalse(t.defined_in_package(ModuleName.of("test.subpackage.sub2_1")))

    def test_type_checks_w_str(self):
        t = type_(AClass)
        self.assertTrue(t.defined_in_module("test.fixtures"))
        self.assertTrue(t.defined_in_package("test.fixtures"))
        self.assertTrue(t.defined_in_package("test"))
        self.assertFalse(t.defined_in_module("test.subpackage"))
        self.assertFalse(t.defined_in_package("test.subpackage"))
        self.assertFalse(t.defined_in_package("test.subpackage.sub2_1"))

    def test_instance_checks_w_module_name(self):
        i = instance(AClass())
        self.assertTrue(i.type_.defined_in_module(ModuleName.of("test.fixtures")))
        self.assertTrue(i.type_.defined_in_package(ModuleName.of("test.fixtures")))
        self.assertTrue(i.type_.defined_in_package(ModuleName.of("test")))
        self.assertFalse(i.type_.defined_in_module(ModuleName.of("test.subpackage")))
        self.assertFalse(i.type_.defined_in_package(ModuleName.of("test.subpackage")))
        self.assertFalse(i.type_.defined_in_package(ModuleName.of("test.subpackage.sub2_1")))

    def test_instance_checks_w_str(self):
        i = instance(AClass())
        self.assertTrue(i.type_.defined_in_module("test.fixtures"))
        self.assertTrue(i.type_.defined_in_package("test.fixtures"))
        self.assertTrue(i.type_.defined_in_package("test"))
        self.assertFalse(i.type_.defined_in_module("test.subpackage"))
        self.assertFalse(i.type_.defined_in_package("test.subpackage"))
        self.assertFalse(i.type_.defined_in_package("test.subpackage.sub2_1"))
