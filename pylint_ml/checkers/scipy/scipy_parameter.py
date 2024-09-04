# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for proper usage of Scipy functions with required parameters."""

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class ScipyParameterChecker(BaseChecker):
    name = "scipy-parameter"
    msgs = {
        "W8111": (
            "Ensure that required parameters %s are explicitly specified in scipy method %s.",
            "scipy-parameter",
            "Explicitly specifying required parameters improves model performance and prevents unintended behavior.",
        ),
    }

    # Define required parameters for specific Scipy classes and methods
    REQUIRED_PARAMS = {
        # scipy.optimize
        "minimize": ["fun", "x0"],
        "curve_fit": ["f", "xdata", "ydata"],
        "root": ["fun", "x0"],
        # scipy.integrate
        "quad": ["func", "a", "b"],
        "dblquad": ["func", "a", "b", "gfun", "hfun"],
        "solve_ivp": ["fun", "t_span", "y0"],
        # scipy.stats
        "ttest_ind": ["a", "b"],
        "ttest_rel": ["a", "b"],
        "norm.pdf": ["x"],
        # scipy.spatial
        "distance.euclidean": ["u", "v"],  # Full chain
        "euclidean": ["u", "v"],  # Direct import of euclidean
        "KDTree.query": ["x"],
    }

    @only_required_for_messages("scipy-parameter")
    def visit_call(self, node: nodes.Call) -> None:
        method_name = self._get_full_method_name(node)
        if method_name in self.REQUIRED_PARAMS:
            provided_keywords = {kw.arg for kw in node.keywords if kw.arg is not None}
            # Collect all missing parameters
            missing_params = [param for param in self.REQUIRED_PARAMS[method_name] if param not in provided_keywords]
            if missing_params:
                self.add_message(
                    "scipy-parameter",
                    node=node,
                    confidence=HIGH,
                    args=(", ".join(missing_params), method_name),
                )

    def _get_full_method_name(self, node: nodes.Call) -> str:
        """
        Extracts the full method name, including handling chained attributes (e.g., scipy.spatial.distance.euclidean)
        and also handles direct imports like euclidean.
        """
        func = node.func
        method_chain = []

        # Traverse the attribute chain to get the full method name
        while isinstance(func, nodes.Attribute):
            method_chain.insert(0, func.attrname)
            func = func.expr

        # If it's a direct function name, like `euclidean`, return it
        if isinstance(func, nodes.Name):
            method_chain.insert(0, func.name)

        return ".".join(method_chain)
