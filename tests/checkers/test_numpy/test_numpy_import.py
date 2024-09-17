import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.numpy.numpy_import import NumpyImportChecker


class TestNumpyImport(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = NumpyImportChecker

    def test_correct_numpy_import(self):
        import_node = astroid.extract_node(
            """
        import numpy as np #@
        """
        )

        with self.assertNoMessages():
            self.checker.visit_import(import_node)

    def test_incorrect_numpy_import(self):
        import_node = astroid.extract_node(
            """
        import numpy as npy #@
        """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="numpy-import",
                confidence=HIGH,
                node=import_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)

    def test_incorrect_numpy_import_from(self):
        importfrom_node = astroid.extract_node(
            """
        from numpy import min #@
        """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="numpy-importfrom",
                confidence=HIGH,
                node=importfrom_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_importfrom(importfrom_node)
