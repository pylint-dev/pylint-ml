import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_dataframe_merge import PandasDataframeMergeChecker


class TestPandasMergeChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasDataframeMergeChecker

    def test_merge_without_explicit_params(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_3 = df_1.merge(df_2)  # [pandas-dataframe-merge]
            """
        )

        merge_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-dataframe-merge",
                confidence=HIGH,
                node=merge_call,
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(merge_call)

    def test_merge_with_missing_validate(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_3 = df_1.merge(df_2, how='inner', on='col1')  # [pandas-dataframe-merge]
            """
        )

        merge_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-dataframe-merge",
                confidence=HIGH,
                node=merge_call,
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(merge_call)

    def test_merge_with_wrong_naming_and_missing_params(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            merged_df = df_1.merge(df_2)  # [pandas-dataframe-merge]
            """
        )

        merge_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-dataframe-merge",
                confidence=HIGH,
                node=merge_call,
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(merge_call)

    def test_merge_with_all_params_and_correct_naming(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_merged = df_1.merge(df_2, how='inner', on='col1', validate='1:1')  # This should not trigger any warnings
            """
        )

        merge_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(merge_call)
