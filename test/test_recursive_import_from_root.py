from unittest import TestCase, main

import test.accumulator
from recursive_import import import_package_recursively

class Test(TestCase):
    def test_importing_from_root(self):
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



if __name__=="__main__":
    main()
