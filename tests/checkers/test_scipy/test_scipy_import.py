import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.scipy.scipy_import import ScipyImportChecker


class TestScipyImport(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = ScipyImportChecker

    def test_correct_scipy_import(self):
        scipy_import_node = astroid.extract_node(
            """
        from scipy.misc import imread, imsave, imresize #@
        """
        )

        with self.assertNoMessages():
            self.checker.visit_import(scipy_import_node)

    def test_incorrect_scipy_import(self):
        scipy_import_node = astroid.extract_node(
            """
        import scipy as spy #@
        """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="scipy-import",
                confidence=HIGH,
                node=scipy_import_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(scipy_import_node)
