import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_dataframe_bool import PandasDataFrameBoolChecker


class TestDataFrameBoolChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasDataFrameBoolChecker

    @patch("pylint_ml.util.library_base_checker.version")
    def test_dataframe_bool_usage(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, call_node = astroid.extract_node(
            """
            import pandas as pd #@
            df_customers = pd.DataFrame(data)
            df_customers.bool() #@
            """
        )
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-dataframe-bool",
                confidence=HIGH,
                node=call_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_call(call_node)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_no_bool_usage(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            df_customers = pd.DataFrame(data)
            df_customers.sum()  #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_call(node)
