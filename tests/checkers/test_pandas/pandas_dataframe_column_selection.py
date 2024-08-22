import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_dataframe_column_selection import PandasColumnSelectionChecker


class TestPandasColumnSelectionChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasColumnSelectionChecker

    def test_incorrect_column_selection(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_sales = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
            value = df_sales.A  # [pandas-column-selection]
            """
        )

        column_attribute = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-column-selection",
                confidence=HIGH,
                node=column_attribute,
            ),
            ignore_position=True,
        ):
            self.checker.visit_attribute(column_attribute)
