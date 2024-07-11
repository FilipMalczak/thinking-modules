from unittest import TestCase, main

import test.accumulator
from recursive_import import import_package_recursively

class Test(TestCase):
    def test_importing_from_root(self):
        test.accumulator.accumulator = []
        import_package_recursively("fixture")
        self.assertEqual(
            [
                'fixture',
                'fixture.x',
                'fixture.y',
                'fixture.sub',
                'fixture.sub.z'
            ],
            test.accumulator.accumulator
        )

    def test_importing_from_subpackage(self):
        test.accumulator.accumulator = []
        import_package_recursively("fixture2.sub")
        self.assertEqual(
            test.accumulator.accumulator,
            [
                "fixture2", # parent packages will get imported by default, not as result of this function
                'fixture2.sub',
                'fixture2.sub.z'
            ]
        )


if __name__=="__main__":
    main()
