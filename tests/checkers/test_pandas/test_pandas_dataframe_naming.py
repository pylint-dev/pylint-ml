import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_dataframe_naming import PandasDataFrameNamingChecker


class TestPandasDataFrameNamingChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasDataFrameNamingChecker

    def test_correct_dataframe_naming(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_customers = pd.DataFrame(data)
            """
        )
        with self.assertNoMessages():
            self.checker.visit_assign(node)

    def test_incorrect_dataframe_naming(self):
        pandas_dataframe_node = astroid.extract_node(
            """
            import pandas as pd
            customers = pd.DataFrame(data)
            """
        )
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-dataframe-naming",
                confidence=HIGH,
                node=pandas_dataframe_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_assign(pandas_dataframe_node)

    def test_incorrect_dataframe_name_length(self):
        pandas_dataframe_node = astroid.extract_node(
            """
            import pandas as pd
            df_ = pd.DataFrame(data)
            """
        )
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-dataframe-naming",
                confidence=HIGH,
                node=pandas_dataframe_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_assign(pandas_dataframe_node)
