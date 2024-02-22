import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.numpy.numpy_nan_comparison import NumpyNaNComparisonChecker


class TestNumpyNaNComparison(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = NumpyNaNComparisonChecker

    def test_singleton_nan_compare(self):
        code = """
        a_nan = np.array([0, 1, np.nan])

        np.nan == a_nan #@

        1 == 1 == np.nan #@

        1 > 0 > np.nan #@

        """
        singleton_nan_compare, chained_nan_compare, great_than_nan_compare = astroid.extract_node(code)

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="numpy-nan-compare",
                node=singleton_nan_compare,
                confidence=HIGH,
            ),
            pylint.testutils.MessageTest(
                msg_id="numpy-nan-compare",
                node=chained_nan_compare,
                confidence=HIGH,
            ),
            pylint.testutils.MessageTest(
                msg_id="numpy-nan-compare",
                node=great_than_nan_compare,
                confidence=HIGH,
            ),
            ignore_position=True,
        ):
            self.checker.visit_compare(singleton_nan_compare)
            self.checker.visit_compare(chained_nan_compare)
            self.checker.visit_compare(great_than_nan_compare)
