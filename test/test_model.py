from unittest import TestCase

from thinking_modules.model import ModuleName, ModuleKind


class ModuleNameTests(TestCase):
    def test_deep_name(self):
        name = ModuleName(["pkg", "subpkg", "mod"])
        self.assertEqual(name.simple, "mod")
        self.assertEqual(name.qualified, "pkg.subpkg.mod")
        self.assertEqual(name.parent, ModuleName(["pkg", "subpkg"]))
        self.assertEqual(name.submodule("sub"), ModuleName(["pkg", "subpkg", "mod", "sub"]))

    def test_module_in_pkg(self):
        name = ModuleName(["pkg", "mod"])
        self.assertEqual(name.simple, "mod")
        self.assertEqual(name.qualified, "pkg.mod")
        self.assertEqual(name.parent, ModuleName(["pkg"]))
        self.assertEqual(name.submodule("sub"), ModuleName(["pkg", "mod", "sub"]))

    def test_unpackaged_module(self):
        name = ModuleName(["mod"])
        self.assertEqual(name.simple, "mod")
        self.assertEqual(name.qualified, "mod")
        self.assertIsNone(name.parent)
        self.assertEqual(name.submodule("sub"), ModuleName(["mod", "sub"]))

    def test_resolving(self):
        mod_name = ModuleName(["x", "y"])
        self.assertEqual(ModuleName.resolve(mod_name), mod_name)
        self.assertEqual(ModuleName.resolve(mod_name.qualified), mod_name)
        self.assertEqual(ModuleName.resolve(mod_name.parts), mod_name)
        from test import fixtures
        self.assertEqual(ModuleName.resolve(fixtures), ModuleName.resolve("test.fixtures"))
        self.assertEqual(ModuleName.resolve(fixtures.AClass), ModuleName.resolve("test.fixtures"))

class ModuleTests(TestCase):
    def test_importing(self):
        name = ModuleName.resolve("test.dontscan.some_module")
        mod = name.module_descriptor
        self.assertFalse(mod.is_imported)
        m = mod.module_object
        self.assertIsNotNone(m)
        self.assertTrue(mod.is_imported)

    def test_describing_packaged_module(self):
        name = ModuleName.resolve("test.subpackage.a_module")
        mod = name.module_descriptor
        from test.subpackage import a_module
        self.assertEqual(mod.name, name)
        self.assertEqual(mod.module_object, a_module)
        self.assertEqual(mod.file_path, a_module.__file__)
        self.assertEqual(mod.kind, ModuleKind.MODULE)
        self.assertFalse(mod.is_package)
        self.assertFalse(mod.is_shell)
        self.assertEqual(mod.root_package_name, ModuleName.resolve("test"))

    def test_describing_subpackage(self):
        name = ModuleName.resolve("test.subpackage")
        mod = name.module_descriptor
        from test import subpackage
        self.assertEqual(mod.name, name)
        self.assertEqual(mod.module_object, subpackage)
        self.assertEqual(mod.file_path, subpackage.__file__)
        self.assertEqual(mod.kind, ModuleKind.PACKAGE)
        self.assertTrue(mod.is_package)
        self.assertFalse(mod.is_shell)
        self.assertEqual(mod.root_package_name, ModuleName.resolve("test"))

    def test_describing_root_package(self):
        name = ModuleName.resolve("test")
        mod = name.module_descriptor
        import test
        self.assertEqual(mod.name, name)
        self.assertEqual(mod.module_object, test)
        self.assertEqual(mod.file_path, test.__file__)
        self.assertEqual(mod.kind, ModuleKind.PACKAGE)
        self.assertTrue(mod.is_package)
        self.assertFalse(mod.is_shell)
        self.assertEqual(mod.root_package_name, ModuleName.resolve("test"))


    def test_describing_package_main(self):
        name = ModuleName.resolve("test.subpackage.__main__")
        mod = name.module_descriptor
        from test.subpackage import __main__
        self.assertEqual(mod.name, name)
        self.assertEqual(mod.module_object, __main__)
        self.assertEqual(mod.file_path, __main__.__file__)
        self.assertEqual(mod.kind, ModuleKind.PACKAGE_MAIN)
        self.assertFalse(mod.is_package)
        self.assertFalse(mod.is_shell)
        self.assertEqual(mod.root_package_name, ModuleName.resolve("test"))

    def test_describing_root_module(self):
        name = ModuleName.resolve("module_fixture")
        mod = name.module_descriptor
        import module_fixture
        self.assertEqual(mod.name, name)
        self.assertEqual(mod.module_object, module_fixture)
        self.assertEqual(mod.file_path, module_fixture.__file__)
        self.assertEqual(mod.kind, ModuleKind.MODULE)
        self.assertFalse(mod.is_package)
        self.assertFalse(mod.is_shell)
        self.assertIsNone(mod.root_package_name)

    def test_canonical(self):
        import os.path
        name = ModuleName.of("os.path")
        #os.path is known to be sys.modules-fuckery based on platform (windows/unix), thus its a good testing target
        self.assertEqual(name.canonical, ModuleName.of(os.path.__name__))
        self.assertFalse(name.is_canonical)

    #shell is not testable from script... sorta by definition