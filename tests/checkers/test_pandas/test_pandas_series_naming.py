import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_series_naming import PandasSeriesNamingChecker


class TestPandasSeriesNamingChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasSeriesNamingChecker

    @patch("pylint_ml.util.library_base_checker.version")
    def test_series_correct_naming(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            ser_sales = pd.Series([100, 200, 300]) #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_assign(node)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_series_incorrect_naming(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            df_sales = pd.Series([100, 200, 300]) #@
            """
        )
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-series-naming",
                confidence=HIGH,
                node=node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_assign(node)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_series_invalid_length_naming(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            ser_ = pd.Series([True]) #@
            """
        )
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-series-naming",
                confidence=HIGH,
                node=node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_assign(node)
