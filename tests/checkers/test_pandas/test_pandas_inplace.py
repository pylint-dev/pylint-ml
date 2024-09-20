import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.pandas.pandas_inplace import PandasInplaceChecker


class TestPandasInplaceChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PandasInplaceChecker

    @patch("pylint_ml.util.library_base_checker.version")
    def test_inplace_used_in_drop(self):
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            df = pd.DataFrame({
                "A": [1, 2, 3],
                "B": [4, 5, 6]
            })
            df.drop(columns=["A"], inplace=True) #@
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
            self.checker.visit_import(import_node)
            self.checker.visit_call(node)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_inplace_used_in_fillna(self):
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            df = pd.DataFrame({
                "A": [1, None, 3],
                "B": [4, 5, None]
            })
            df.fillna(0, inplace=True) #@
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
            self.checker.visit_import(import_node)
            self.checker.visit_call(node)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_inplace_used_in_sort_values(self):
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            df = pd.DataFrame({
                "A": [3, 2, 1],
                "B": [4, 5, 6]
            })
            df.sort_values(by="A", inplace=True) #@
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
            self.checker.visit_import(import_node)
            self.checker.visit_call(node)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_no_inplace(self):
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            df = pd.DataFrame({
                "A": [1, 2, 3],
                "B": [4, 5, 6]
            })
            df = df.drop(columns=["A"]) #@
            """
        )

        inplace_call = node.value

        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_call(inplace_call)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_inplace_used_in_unsupported_method(self):
        import_node, node = astroid.extract_node(
            """
            import pandas as pd #@
            df = pd.DataFrame({
                "A": [1, 2, 3],
                "B": [4, 5, 6]
            })
            df.append({"A": 4, "B": 7}, inplace=True) #@
            """
        )

        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_call(node)
