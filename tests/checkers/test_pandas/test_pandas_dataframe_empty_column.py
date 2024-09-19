import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_dataframe_empty_column import PandasEmptyColumnChecker


class TestPandasEmptyColumnChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasEmptyColumnChecker

    def test_correct_empty_column_initialization(self):
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

    def test_incorrect_empty_column_initialization_with_zero(self):
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

    def test_incorrect_empty_column_initialization_with_empty_string(self):
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
