from unittest import TestCase, main

import test.accumulator
from thinking_modules.importing import import_package_recursively
from thinking_modules.model import ModuleName


class Test(TestCase):
    def test_importing_from_root(self):
        result = import_package_recursively("fixture")
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
        self.assertEqual(
            [
                ModuleName.resolve(x)
                for x in [
                    'fixture',
                    'fixture.x',
                    'fixture.y',
                    'fixture.sub',
                    'fixture.sub.z'
                ]
            ],
            result
        )



if __name__=="__main__":
    main()
