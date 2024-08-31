from unittest import TestCase

from thinking_modules.model import ModuleName
from thinking_modules.scan import scan


class ScanningTests(TestCase):
    def test_scanning_wo_main(self):
        results = list(scan("test.subpackage"))
        expected = [
            ModuleName.of('test.subpackage'),
            ModuleName.of('test.subpackage.a_module'),
            ModuleName.of('test.subpackage.sub2_1'),
            ModuleName.of('test.subpackage.sub2_1.a'),
            ModuleName.of('test.subpackage.sub2_1.b'),
            ModuleName.of('test.subpackage.sub2_1.sub3'),
            ModuleName.of('test.subpackage.sub2_1.sub3.c'),
            ModuleName.of('test.subpackage.sub2_1.sub3.d'),
            ModuleName.of('test.subpackage.sub2_1.sub3.e'),
            ModuleName.of('test.subpackage.sub2_2'),
            ModuleName.of('test.subpackage.sub2_2.a'),
            ModuleName.of('test.subpackage.sub2_2.b'),
            ModuleName.of('test.subpackage.sub2_2.sub3'),
            ModuleName.of('test.subpackage.sub2_2.sub3.c'),
            ModuleName.of('test.subpackage.sub2_2.sub3.d'),
            ModuleName.of('test.subpackage.sub2_2.sub3.e')
        ]
        self.assertSequenceEqual(expected, results)


    def test_scanning_including_main(self):
        results = list(scan("test.subpackage", include_mains=True))
        expected = [
            ModuleName.of('test.subpackage'),
            ModuleName.of('test.subpackage.__main__'),
            ModuleName.of('test.subpackage.a_module'),
            ModuleName.of('test.subpackage.sub2_1'),
            ModuleName.of('test.subpackage.sub2_1.a'),
            ModuleName.of('test.subpackage.sub2_1.b'),
            ModuleName.of('test.subpackage.sub2_1.sub3'),
            ModuleName.of('test.subpackage.sub2_1.sub3.__main__'),
            ModuleName.of('test.subpackage.sub2_1.sub3.c'),
            ModuleName.of('test.subpackage.sub2_1.sub3.d'),
            ModuleName.of('test.subpackage.sub2_1.sub3.e'),
            ModuleName.of('test.subpackage.sub2_2'),
            ModuleName.of('test.subpackage.sub2_2.a'),
            ModuleName.of('test.subpackage.sub2_2.b'),
            ModuleName.of('test.subpackage.sub2_2.sub3'),
            ModuleName.of('test.subpackage.sub2_2.sub3.__main__'),
            ModuleName.of('test.subpackage.sub2_2.sub3.c'),
            ModuleName.of('test.subpackage.sub2_2.sub3.d'),
            ModuleName.of('test.subpackage.sub2_2.sub3.e')
        ]
        self.assertSequenceEqual(expected, results)
