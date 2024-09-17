import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_import import PandasImportChecker


class TestPandasImport(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasImportChecker

    def test_correct_pandas_import(self):
        pandas_import_node = astroid.extract_node(
            """
            import pandas as pd #@
            """
        )

        with self.assertNoMessages():
            self.checker.visit_import(pandas_import_node)

    def test_incorrect_pandas_import(self):
        pandas_import_node = astroid.extract_node(
            """
            import pandas as pds #@
            """
        )

        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="pandas-import",
                    confidence=HIGH,
                    node=pandas_import_node,
                ),
                ignore_position=True,
        ):
            self.checker.visit_import(pandas_import_node)

    def test_incorrect_pandas_import_from(self):
        pandas_importfrom_node = astroid.extract_node(
            """
            from pandas import math #@
            """
        )

        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="pandas-importfrom",
                    confidence=HIGH,
                    node=pandas_importfrom_node,
                ),
                ignore_position=True,
        ):
            self.checker.visit_importfrom(pandas_importfrom_node)
