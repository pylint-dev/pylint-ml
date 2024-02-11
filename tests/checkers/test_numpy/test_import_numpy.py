import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.numpy.import_numpy import NumpyImportChecker


class TestNumpyImport(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = NumpyImportChecker

    def test_correct_numpy_import(self):
        numpy_import_node = astroid.extract_node(
            """
        import numpy as np
        """
        )

        with self.assertNoMessages():
            self.checker.visit_import(numpy_import_node)

    def test_incorrect_numpy_import(self):
        numpy_import_node = astroid.extract_node(
            """
        import numpy as npy
        """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="numpy-import",
                confidence=HIGH,
                node=numpy_import_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(numpy_import_node)

    def test_incorrect_numpy_import_from(self):
        numpy_importfrom_node = astroid.extract_node(
            """
        from numpy import min
        """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="numpy-importfrom",
                confidence=HIGH,
                node=numpy_importfrom_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_importfrom(numpy_importfrom_node)
