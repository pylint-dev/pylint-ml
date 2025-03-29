# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for proper usage of Scipy functions with required parameters."""

from astroid import nodes
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

from pylint_ml.checkers.config import SCIPY
from pylint_ml.checkers.library_base_checker import LibraryBaseChecker


class ScipyParameterChecker(LibraryBaseChecker):
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
        "pdf": ["x"],
        # scipy.spatial
        "euclidean": ["u", "v"],
        "query": ["x"],
    }

    @only_required_for_messages("scipy-parameter")
    def visit_call(self, node: nodes.Call) -> None:
        if not self.is_library_imported_and_version_valid(lib_name=SCIPY, required_version=None):
            return

        # Determine whether the function is a simple Name (method call)
        if isinstance(node.func, nodes.Name):
            method_name = node.func.name  # For cases like minimize()
        else:
            return  # Exit early

        # Perform a lookup in the current scope for the function/method name
        scope = node.scope()
        name_lookup = scope.lookup(method_name)

        if name_lookup:
            _, assignments = name_lookup
            if assignments:
                assignment = assignments[0]
                if isinstance(assignment, nodes.ImportFrom):
                    # Check if the import is from scipy.optimize
                    # Correctly unpack the names from the tuple
                    imported_names = [name for name, _ in assignment.names]

                    if SCIPY in assignment.modname and method_name in imported_names:
                        # Proceed with checking parameters
                        if method_name in self.REQUIRED_PARAMS:
                            provided_keywords = {kw.arg for kw in node.keywords if kw.arg is not None}
                            missing_params = [
                                param for param in self.REQUIRED_PARAMS[method_name] if param not in provided_keywords
                            ]

                            if missing_params:
                                self.add_message(
                                    "scipy-parameter",
                                    node=node,
                                    confidence=HIGH,
                                    args=(", ".join(missing_params), method_name),
                                )
