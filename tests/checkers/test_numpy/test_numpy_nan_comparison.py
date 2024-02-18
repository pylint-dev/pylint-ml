import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.numpy.numpy_nan_comparison import NumpyNaNComparisonChecker


class TestNumpyNaNComparison(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = NumpyNaNComparisonChecker

    def test_correct_nan_compare(self):
        nan_compare_node = astroid.extract_node(
            """
        np.isnan(np.nan)
        """
        )

        with self.assertNoMessages():
            self.checker.visit_compare(nan_compare_node)

    def test_incorrect_nan_compare(self):
        nan_compare_node = astroid.extract_node(
            """
        a_nan = np.array([0, 1, np.nan])
        print(a_nan)
        # [ 0.  1. nan]

        print(a_nan == np.nan)
        # [False False False]

        print(np.isnan(a_nan))
        # [False False  True]

        print(a_nan > 0)
        # [False  True False]
        """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="numpy-nan-compare",
                confidence=HIGH,
                node=nan_compare_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_compare(nan_compare_node)
