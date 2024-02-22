import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.sklearn.sklearn_import import SklearnImportChecker


class TestSklearnImport(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = SklearnImportChecker

    def test_correct_sklearn_import(self):
        sklearn_import_node = astroid.extract_node(
            """
        from sklearn import datasets
        """
        )

        with self.assertNoMessages():
            self.checker.visit_import(sklearn_import_node)

    def test_incorrect_sklearn_import(self):
        sklearn_import_node = astroid.extract_node(
            """
        import sklearn as skl
        """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="sklearn-import",
                confidence=HIGH,
                node=sklearn_import_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(sklearn_import_node)
