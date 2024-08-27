from unittest import TestCase, main

import test.accumulator
from thinking_modules.importing import import_package_recursively
from thinking_modules.model import ModuleName


class Test(TestCase):

    def test_importing_from_subpackage(self):
        result = import_package_recursively("fixture2.sub")
        self.assertEqual(
            [
                "fixture2", # parent packages will get imported by default, not as result of this function
                'fixture2.sub',
                'fixture2.sub.z'
            ],
            test.accumulator.accumulator
        )
        self.assertEqual(
            [
                ModuleName.resolve(x)
                for x in [
                    'fixture2.sub',
                    'fixture2.sub.z'
                ]
            ],
            result
        )


if __name__=="__main__":
    main()
