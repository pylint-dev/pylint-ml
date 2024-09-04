import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_parameter import PandasParameterChecker


class TestPandasParameterChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasParameterChecker

    def test_dataframe_missing_data(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_yoda = pd.DataFrame()  # [pandas-parameter]
            """
        )

        dataframe_call = node.value

        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="pandas-parameter",
                    confidence=HIGH,
                    node=dataframe_call,
                    args=("data", "DataFrame"),
                ),
                ignore_position=True,
        ):
            self.checker.visit_call(dataframe_call)

    def test_merge_without_required_params(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_yoda1 = pd.DataFrame({'A': [1, 2]})
            df_yoda2 = pd.DataFrame({'A': [3, 4]})
            df_yoda_merged = df_yoda1.merge(df_yoda2)  # [pandas-parameter]
            """
        )

        merge_call = node.value

        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="pandas-parameter",
                    confidence=HIGH,
                    node=merge_call,
                    args=("right, how, on, validate", "merge"),
                ),
                ignore_position=True,
        ):
            self.checker.visit_call(merge_call)

    def test_read_csv_without_filepath(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_yoda = pd.read_csv()  # [pandas-parameter]
            """
        )

        read_csv_call = node.value

        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="pandas-parameter",
                    confidence=HIGH,
                    node=read_csv_call,
                    args=("filepath_or_buffer, dtype", "read_csv"),
                ),
                ignore_position=True,
        ):
            self.checker.visit_call(read_csv_call)

    def test_to_csv_without_path(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_yoda = pd.DataFrame({'A': [1, 2]})
            df_yoda.to_csv()  # [pandas-parameter]
            """
        )

        to_csv_call = node

        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="pandas-parameter",
                    confidence=HIGH,
                    node=to_csv_call,
                    args=("path_or_buf", "to_csv"),
                ),
                ignore_position=True,
        ):
            self.checker.visit_call(to_csv_call)

    def test_groupby_without_by(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_yoda = pd.DataFrame({'A': [1, 2]})
            df_yoda.groupby()  # [pandas-parameter]
            """
        )

        groupby_call = node

        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="pandas-parameter",
                    confidence=HIGH,
                    node=groupby_call,
                    args=("by", "groupby"),
                ),
                ignore_position=True,
        ):
            self.checker.visit_call(groupby_call)

    def test_fillna_without_value(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_yoda = pd.DataFrame({'A': [1, None]})
            df_yoda.fillna()  # [pandas-parameter]
            """
        )

        fillna_call = node

        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="pandas-parameter",
                    confidence=HIGH,
                    node=fillna_call,
                    args=("value", "fillna"),
                ),
                ignore_position=True,
        ):
            self.checker.visit_call(fillna_call)

    def test_sort_values_without_by(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_yoda = pd.DataFrame({'A': [1, 2]})
            df_yoda.sort_values()  # [pandas-parameter]
            """
        )

        sort_values_call = node

        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="pandas-parameter",
                    confidence=HIGH,
                    node=sort_values_call,
                    args=("by", "sort_values"),
                ),
                ignore_position=True,
        ):
            self.checker.visit_call(sort_values_call)

    def test_merge_with_missing_validate(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_3 = df_1.merge(right=df_2, how='inner', on='col1')  # [pandas-dataframe-merge]
            """
        )

        merge_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-parameter",
                confidence=HIGH,
                node=merge_call,
                args=('validate', 'merge'),
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(merge_call)

    def test_merge_with_wrong_naming_and_missing_params(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            merged_df = df_1.merge(right=df_2)  # [pandas-dataframe-merge]
            """
        )

        merge_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-parameter",
                confidence=HIGH,
                node=merge_call,
                args=('how, on, validate', 'merge')
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(merge_call)

    def test_merge_with_all_params_and_correct_naming(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df_merged = df_1.merge(right=df_2, how='inner', on='col1', validate='1:1')  # This should not trigger any warnings
            """
        )

        merge_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(merge_call)
