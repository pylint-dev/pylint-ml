# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for proper usage of numpy functions with required parameters."""

from astroid import nodes
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

from pylint_ml.util.common import get_full_method_name
from pylint_ml.util.config import LIB_NUMPY
from pylint_ml.util.library_base_checker import LibraryBaseChecker


class NumPyParameterChecker(LibraryBaseChecker):
    name = "numpy-parameter"
    msgs = {
        "W8111": (
            "Ensure that required parameters %s are explicitly specified in numpy method %s.",
            "numpy-parameter",
            "Explicitly specifying required parameters improves model performance and prevents unintended behavior.",
        ),
    }

    REQUIRED_PARAMS = {
        # Array Creation
        "array": ["object"],
        "zeros": ["shape"],
        "ones": ["shape"],
        "full": ["shape", "fill_value"],
        "empty": ["shape"],
        "arange": ["start"],
        "linspace": ["start", "stop"],
        "logspace": ["start", "stop"],
        "eye": ["N"],
        "identity": ["n"],
        # Random Sampling
        "random.rand": ["d0"],
        "random.randn": ["d0"],
        "random.randint": ["low", "high"],
        "random.choice": ["a"],
        "random.uniform": ["low", "high"],
        "random.normal": ["loc", "scale"],
        # Mathematical Functions
        "sum": ["a"],
        "mean": ["a"],
        "median": ["a"],
        "std": ["a"],
        "var": ["a"],
        "prod": ["a"],
        "min": ["a"],
        "max": ["a"],
        "ptp": ["a"],
        # Array Manipulation
        "reshape": ["newshape"],
        "transpose": [],
        "concatenate": ["arrays"],
        "stack": ["arrays"],
        "vstack": ["arrays"],
        "hstack": ["arrays"],
        # Linear Algebra
        "dot": ["a", "b"],
        "matmul": ["a", "b"],
        "linalg.inv": ["a"],
        "linalg.eig": ["a"],
        "linalg.solve": ["a", "b"],
        # Statistical Functions
        "percentile": ["a", "q"],
        "quantile": ["a", "q"],
        "corrcoef": ["x"],
        "cov": ["m"],
    }

    @only_required_for_messages("numpy-parameter")
    def visit_call(self, node: nodes.Call) -> None:
        if not self.is_library_imported_and_version_valid(lib_name=LIB_NUMPY, required_version=None):
            return

        method_name = get_full_method_name(node)
        if method_name in self.REQUIRED_PARAMS:
            provided_keywords = {kw.arg for kw in node.keywords if kw.arg is not None}
            missing_params = [param for param in self.REQUIRED_PARAMS[method_name] if param not in provided_keywords]
            if missing_params:
                self.add_message(
                    "numpy-parameter",
                    node=node,
                    confidence=HIGH,
                    args=(", ".join(missing_params), method_name),
                )
