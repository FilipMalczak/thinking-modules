from unittest import TestCase

from thinking_modules.main_module import main_module, main_name
from thinking_modules.model import ModuleName


class MainModuleTest(TestCase):
    def test_main(self):
        #this will only pass if executed as 'python -m unittest'
        self.assertEqual(main_name, ModuleName.of("unittest.__main__"))
        self.assertTrue(main_module.is_main)
        self.assertEqual(main_name.canonical, ModuleName.of("__main__"))
        self.assertFalse(main_module.name.is_canonical)
