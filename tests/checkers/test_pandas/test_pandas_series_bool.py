import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_series_bool import PandasSeriesBoolChecker


class TestSeriesBoolChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasSeriesBoolChecker

    def test_series_bool_usage(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            series = pd.Series(data)
            series.bool()  # [pandas-series-bool]
            """
        )
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-series-bool",
                confidence=HIGH,
                node=node,
            )
        ):
            self.checker.visit_call(node)

    def test_no_bool_usage(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            series = pd.Series(data)
            series.sum()  # This should pass without warnings
            """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)
