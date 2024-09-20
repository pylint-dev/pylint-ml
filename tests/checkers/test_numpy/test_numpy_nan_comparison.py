from unittest.mock import patch

import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.numpy.numpy_nan_comparison import NumpyNaNComparisonChecker


class TestNumpyNaNComparison(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = NumpyNaNComparisonChecker

    @patch("pylint_ml.util.library_base_checker.version")
    def test_singleton_nan_compare(self, mock_version):
        mock_version.return_value = "2.1.1"
        import_node, singleton_node, chained_node, great_than_node = astroid.extract_node(
            """
        import numpy as np #@

        a_nan = np.array([0, 1, np.nan])
        np.nan == a_nan #@
        1 == 1 == np.nan #@
        1 > 0 > np.nan #@
        """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="numpy-nan-compare",
                node=singleton_node,
                confidence=HIGH,
            ),
            pylint.testutils.MessageTest(
                msg_id="numpy-nan-compare",
                node=chained_node,
                confidence=HIGH,
            ),
            pylint.testutils.MessageTest(
                msg_id="numpy-nan-compare",
                node=great_than_node,
                confidence=HIGH,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_compare(singleton_node)
            self.checker.visit_compare(chained_node)
            self.checker.visit_compare(great_than_node)
