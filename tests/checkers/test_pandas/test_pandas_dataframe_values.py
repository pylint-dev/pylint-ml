import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_dataframe_values import PandasValuesChecker


class TestPandasValuesChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasValuesChecker

    def test_values_usage_with_correct_naming(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_sales = pd.DataFrame({
                "A": [1, 2, 3],
                "B": [4, 5, 6]
            })
            data = df_sales.values  #@
            """
        )

        # Access the attribute that is 'values'
        attribute_node = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-dataframe-values",
                confidence=HIGH,
                node=attribute_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_attribute(attribute_node)
