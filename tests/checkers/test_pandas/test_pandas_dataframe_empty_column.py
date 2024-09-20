import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_dataframe_empty_column import PandasEmptyColumnChecker


class TestPandasEmptyColumnChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasEmptyColumnChecker

    @patch("pylint_ml.util.library_base_checker.version")
    def test_correct_empty_column_initialization(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            df_sales = pd.DataFrame()
            df_sales['new_col_str'] = pd.Series(dtype='object')  #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_subscript(node)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_incorrect_empty_column_initialization_with_zero(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            df_sales = pd.DataFrame()
            df_sales['new_col_int'] = 0  #@
            """
        )

        subscript_node = node.targets[0]

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-dataframe-empty-column",
                confidence=HIGH,
                node=subscript_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_subscript(subscript_node)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_incorrect_empty_column_initialization_with_empty_string(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            df_sales = pd.DataFrame()
            df_sales['new_col_str'] = '' #@
            """
        )

        subscript_node = node.targets[0]

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-dataframe-empty-column",
                confidence=HIGH,
                node=subscript_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_subscript(subscript_node)
