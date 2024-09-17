# from pylint.testutils import CheckerTestCase
# from astroid import nodes
# from pylint_ml.util.library_handler import LibraryHandler
#
#
# class TestLibraryHandler(CheckerTestCase):
#
#     def setUp(self):
#         super().setUp()
#         self.checker = LibraryHandler(self.linter)
#
#     def test_visit_import(self):
#         # Simulating an import statement like `import numpy as np`
#         node = nodes.Import(names=[('numpy', 'np')])
#         self.checker.visit_import(node)
#
#         # Assert that `np` is recognized as `numpy`
#         self.assertIn('np', self.checker.imports)
#         self.assertEqual(self.checker.imports['np'], 'numpy')
#
#     def test_visit_importfrom(self):
#         # Simulating an import from statement like `from pandas import DataFrame`
#         node = nodes.ImportFrom(modname='pandas', names=[('DataFrame', None)], level=0)
#         self.checker.visit_importfrom(node)
#
#         # Assert that `DataFrame` is recognized as `pandas.DataFrame`
#         self.assertIn('DataFrame', self.checker.imports)
#         self.assertEqual(self.checker.imports['DataFrame'], 'pandas.DataFrame')
#
#     def test_is_library_imported(self):
#         # Simulating some imports
#         node = nodes.Import(names=[('numpy', 'np')])
#         self.checker.visit_import(node)
#         node = nodes.ImportFrom(modname='pandas', names=[('DataFrame', None)], level=0)
#         self.checker.visit_importfrom(node)
#
#         # Checking if libraries are imported correctly
#         self.assertTrue(self.checker.is_library_imported('numpy'))
#         self.assertTrue(self.checker.is_library_imported('pandas'))
#         self.assertFalse(self.checker.is_library_imported('sklearn'))
