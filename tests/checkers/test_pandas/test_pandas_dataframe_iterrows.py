import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_dataframe_iterrows import PandasIterrowsChecker


class TestPandasIterrowsChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasIterrowsChecker

    def test_iterrows_used(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_sales = pd.DataFrame({
                "Product": ["A", "B", "C"],
                "Sales": [100, 200, 300]
            })
            for index, row in df_sales.iterrows():  # [pandas-iterrows]
                print(row["Product"], row["Sales"])
            """
        )

        # Extract the Call node for the `iterrows` method
        iterrows_call = node.iter  # This directly points to the `Call` node for `iterrows()`

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-iterrows",
                confidence=HIGH,
                node=iterrows_call,
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(iterrows_call)
