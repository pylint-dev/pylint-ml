import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_dataframe_column_selection import PandasColumnSelectionChecker


class TestPandasColumnSelectionChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasColumnSelectionChecker

    @patch("pylint_ml.util.library_base_checker.version")
    def test_incorrect_column_selection(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            df_sales = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
            value = df_sales.A  #@
            """
        )

        attribute_node = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-column-selection",
                confidence=HIGH,
                node=attribute_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_attribute(attribute_node)
