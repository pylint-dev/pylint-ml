from unittest.mock import patch

import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.numpy.numpy_parameter import NumPyParameterChecker


class TestNumPyParameterChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = NumPyParameterChecker

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_array_missing_object(self, mock_version):
        mock_version.return_value = "2.1.1"
        import_node, call_node = astroid.extract_node(
            """
            import numpy as np #@
            arr = np.array()  #@
            """
        )

        call_node = call_node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="numpy-parameter",
                confidence=HIGH,
                node=call_node,
                args=("object", "array"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_call(call_node)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_zeros_without_shape(self, mock_version):
        mock_version.return_value = "2.1.1"
        import_node, node = astroid.extract_node(
            """
            import numpy as np #@
            arr = np.zeros()  #@
            """
        )

        zeros_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="numpy-parameter",
                confidence=HIGH,
                node=zeros_call,
                args=("shape", "zeros"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_call(zeros_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_random_rand_without_shape(self, mock_version):
        mock_version.return_value = "2.1.1"
        import_node, node = astroid.extract_node(
            """
            import numpy as np #@
            arr = np.random.rand() #@
            """
        )

        rand_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="numpy-parameter",
                confidence=HIGH,
                node=rand_call,
                args=("d0", "rand"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_call(rand_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_dot_without_b(self, mock_version):
        mock_version.return_value = "2.1.1"
        import_node, node = astroid.extract_node(
            """
            import numpy as np #@
            arr = np.dot(a=[1, 2, 3]) #@
            """
        )

        dot_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="numpy-parameter",
                confidence=HIGH,
                node=dot_call,
                args=("b", "dot"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_call(dot_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_percentile_without_q(self, mock_version):
        mock_version.return_value = "2.1.1"
        import_node, node = astroid.extract_node(
            """
            import numpy as np #@
            result = np.percentile(a=[1, 2, 3]) #@
            """
        )

        percentile_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="numpy-parameter",
                confidence=HIGH,
                node=percentile_call,
                args=("q", "percentile"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_call(percentile_call)
