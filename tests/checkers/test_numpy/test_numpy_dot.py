import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.numpy.numpy_dot import NumpyDotChecker


class TestNumpyDotChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = NumpyDotChecker

    def test_warning_for_dot(self):
        import_np, node = astroid.extract_node(
            """
        import numpy as np #@
        a = np.array([1, 2])
        b = np.array([3, 4])
        np.dot(a, b) #@
        """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="numpy-dot-usage",
                node=node,
                confidence=HIGH,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_np)
            self.checker.visit_call(node)
