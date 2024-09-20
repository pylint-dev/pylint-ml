import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_dataframe_naming import PandasDataFrameNamingChecker


class TestPandasDataFrameNamingChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasDataFrameNamingChecker

    @patch("pylint_ml.util.library_base_checker.version")
    def test_correct_dataframe_naming(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            df_customers = pd.DataFrame(data) #@
            """
        )
        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_assign(node)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_incorrect_dataframe_naming(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, pandas_dataframe_node = astroid.extract_node(
            """
            import pandas as pd #@
            customers = pd.DataFrame(data) #@
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
            self.checker.visit_import(import_node)
            self.checker.visit_assign(pandas_dataframe_node)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_incorrect_dataframe_name_length(self, mock_version):
        mock_version.return_value = "2.2.2"
        import_node, pandas_dataframe_node = astroid.extract_node(
            """
            import pandas as pd #@
            df_ = pd.DataFrame(data) #@
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
            self.checker.visit_import(import_node)
            self.checker.visit_assign(pandas_dataframe_node)
