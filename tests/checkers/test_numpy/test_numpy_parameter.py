import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.numpy.numpy_parameter import NumPyParameterChecker


class TestNumPyParameterChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = NumPyParameterChecker

    def test_array_missing_object(self):
        node = astroid.extract_node(
            """
            import numpy as np
            arr = np.array()  # [numpy-parameter]
            """
        )

        array_call = node.value

        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="numpy-parameter",
                    confidence=HIGH,
                    node=array_call,
                    args=("object", "array"),
                ),
                ignore_position=True,
        ):
            self.checker.visit_call(array_call)

    def test_zeros_without_shape(self):
        node = astroid.extract_node(
            """
            import numpy as np
            arr = np.zeros()  # [numpy-parameter]
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
            self.checker.visit_call(zeros_call)

    def test_random_rand_without_shape(self):
        node = astroid.extract_node(
            """
            import numpy as np
            arr = np.random.rand()  # [numpy-parameter]
            """
        )

        rand_call = node.value

        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="numpy-parameter",
                    confidence=HIGH,
                    node=rand_call,
                    args=("d0", "random.rand"),
                ),
                ignore_position=True,
        ):
            self.checker.visit_call(rand_call)

    def test_dot_without_b(self):
        node = astroid.extract_node(
            """
            import numpy as np
            arr = np.dot(a=[1, 2, 3])  # [numpy-parameter]
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
            self.checker.visit_call(dot_call)

    def test_percentile_without_q(self):
        node = astroid.extract_node(
            """
            import numpy as np
            result = np.percentile(a=[1, 2, 3])  # [numpy-parameter]
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
            self.checker.visit_call(percentile_call)
