from unittest.mock import patch

import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.scipy.scipy_parameter import ScipyParameterChecker


class TestScipyParameterChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = ScipyParameterChecker

    # TODO CONTINUE WITH MOCK FOR ALL TESTS
    @patch("pylint_ml.util.library_base_checker.version")
    def test_minimize_params(self, mock_version):
        mock_version.return_value = "1.7.0"
        importfrom_node, node = astroid.extract_node(
            """
            from scipy.optimize import minimize #@
            result = minimize(x0=[1, 2, 3]) #@
            """
        )
        minimize_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="scipy-parameter",
                confidence=HIGH,
                node=minimize_call,
                args=("fun", "minimize"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_importfrom(importfrom_node)
            self.checker.visit_call(minimize_call)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_curve_fit_params(self, mock_version):
        mock_version.return_value = "1.7.0"
        importfrom_node, node = astroid.extract_node(
            """
            from scipy.optimize import curve_fit #@
            params = curve_fit(xdata=[1, 2, 3], ydata=[4, 5, 6])  #@
            """
        )
        curve_fit_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="scipy-parameter",
                confidence=HIGH,
                node=curve_fit_call,
                args=("f", "curve_fit"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_importfrom(importfrom_node)
            self.checker.visit_call(curve_fit_call)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_quad_params(self, mock_version):
        mock_version.return_value = "1.7.0"
        importfrom_node, node = astroid.extract_node(
            """
            from scipy.integrate import quad #@
            result = quad(a=0, b=1)  #@
            """
        )
        quad_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="scipy-parameter",
                confidence=HIGH,
                node=quad_call,
                args=("func", "quad"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_importfrom(importfrom_node)
            self.checker.visit_call(quad_call)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_solve_ivp_params(self, mock_version):
        mock_version.return_value = "1.7.0"
        importfrom_node, node = astroid.extract_node(
            """
            from scipy.integrate import solve_ivp #@
            result = solve_ivp(fun=None, t_span=[0, 1])  #@
            """
        )
        solve_ivp_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="scipy-parameter",
                confidence=HIGH,
                node=solve_ivp_call,
                args=("y0", "solve_ivp"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_importfrom(importfrom_node)
            self.checker.visit_call(solve_ivp_call)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_ttest_ind_params(self, mock_version):
        mock_version.return_value = "1.7.0"
        importfrom_node, node = astroid.extract_node(
            """
            from scipy.stats import ttest_ind #@
            result = ttest_ind(a=[1, 2])  #@
            """
        )
        ttest_ind_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="scipy-parameter",
                confidence=HIGH,
                node=ttest_ind_call,
                args=("b", "ttest_ind"),  # The missing parameter and method name, as formatted by the checker
            ),
            ignore_position=True,
        ):
            self.checker.visit_importfrom(importfrom_node)
            self.checker.visit_call(ttest_ind_call)

    @patch("pylint_ml.util.library_base_checker.version")
    def test_euclidean_params(self, mock_version):
        mock_version.return_value = "1.7.0"
        importfrom_node, node = astroid.extract_node(
            """
            from scipy.spatial.distance import euclidean #@
            dist = euclidean(u=[1, 2, 3])  #@
            """
        )
        euclidean_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="scipy-parameter",
                confidence=HIGH,
                node=euclidean_call,
                args=("v", "euclidean"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_importfrom(importfrom_node)
            self.checker.visit_call(euclidean_call)
