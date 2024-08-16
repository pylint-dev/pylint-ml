import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_dataframe_bool import PandasDataFrameBoolChecker


class TestDataFrameBoolChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasDataFrameBoolChecker

    def test_dataframe_bool_usage(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_customers = pd.DataFrame(data)
            df_customers.bool()  # [pandas-dataframe-bool]
            """
        )
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-dataframe-bool",
                confidence=HIGH,
                node=node,
            )
        ):
            self.checker.visit_call(node)

    def test_no_bool_usage(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_customers = pd.DataFrame(data)
            df_customers.sum()  # This should pass without warnings
            """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)
