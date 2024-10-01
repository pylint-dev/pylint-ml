from unittest.mock import patch

import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_series_bool import PandasSeriesBoolChecker


class TestSeriesBoolChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasSeriesBoolChecker

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_series_bool_usage(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            ser_customer = pd.Series(data)
            ser_customer.bool() #@
            """
        )
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-series-bool",
                confidence=HIGH,
                node=node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_call(node)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_no_bool_usage(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            ser_customer = pd.Series(data)
            ser_customer.sum() #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_call(node)
