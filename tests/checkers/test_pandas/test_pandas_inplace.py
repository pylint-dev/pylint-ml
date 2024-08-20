import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_inplace import PandasInplaceChecker


class TestPandasInplaceChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasInplaceChecker

    def test_inplace_used_in_drop(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df = pd.DataFrame({
                "A": [1, 2, 3],
                "B": [4, 5, 6]
            })
            df.drop(columns=["A"], inplace=True)  # [pandas-inplace]
            """
        )
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-inplace",
                confidence=HIGH,
                node=node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(node)

    def test_inplace_used_in_fillna(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df = pd.DataFrame({
                "A": [1, None, 3],
                "B": [4, 5, None]
            })
            df.fillna(0, inplace=True)  # [pandas-inplace]
            """
        )
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-inplace",
                confidence=HIGH,
                node=node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(node)

    def test_inplace_used_in_sort_values(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df = pd.DataFrame({
                "A": [3, 2, 1],
                "B": [4, 5, 6]
            })
            df.sort_values(by="A", inplace=True)  # [pandas-inplace]
            """
        )
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pandas-inplace",
                confidence=HIGH,
                node=node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(node)

    def test_no_inplace(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df = pd.DataFrame({
                "A": [1, 2, 3],
                "B": [4, 5, 6]
            })
            df = df.drop(columns=["A"])  # This should not trigger any warnings
            """
        )

        inplace_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(inplace_call)

    def test_inplace_used_in_unsupported_method(self):
        node = astroid.extract_node(
            """
            import pandas as pd
            df = pd.DataFrame({
                "A": [1, 2, 3],
                "B": [4, 5, 6]
            })
            df.append({"A": 4, "B": 7}, inplace=True)  # This should not trigger any warnings
            """
        )

        with self.assertNoMessages():
            self.checker.visit_call(node)
