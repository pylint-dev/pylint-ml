import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_dtype_param import PandasDtypeChecker


class TestPandasDtypeChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasDtypeChecker

    def test_dtype_specified(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df = pd.read_csv('file.csv', dtype={'column1': 'int32'})
            """
        )

        dtype_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(node.value)

    def test_dtype_missing(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_sales = pd.read_csv('file.csv')
            """
        )

        dtype_call = node.value

        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="pandas-dtype-param",
                    confidence=HIGH,
                    node=dtype_call,
                ),
                ignore_position=True,
        ):
            self.checker.visit_call(dtype_call)
