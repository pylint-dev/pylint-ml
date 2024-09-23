# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for the use of np.dot and recommend np.matmul for matrix multiplication."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

from pylint_ml.checkers.config import NUMPY
from pylint_ml.checkers.library_base_checker import LibraryBaseChecker


class NumpyDotChecker(LibraryBaseChecker):
    name = "numpy-dot-checker"
    msgs = {
        "W8122": (
            "Consider using 'np.matmul()' instead of 'np.dot()' for matrix multiplication.",
            "numpy-dot-usage",
            "It's recommended to use 'np.matmul()' for matrix multiplication, which is more explicit and handles "
            "higher-dimensional arrays more consistently. ",
        ),
    }

    def visit_import(self, node: nodes.Import):
        super().visit_import(node=node)

    @only_required_for_messages("numpy-dot-usage")
    def visit_call(self, node: nodes.Call) -> None:
        if not self.is_library_imported_and_version_valid(lib_name=NUMPY, required_version=None):
            return

        # Check if the function being called is np.dot
        if isinstance(node.func, nodes.Attribute):
            func_name = node.func.attrname
            module_name = getattr(node.func.expr, "name", None)

            if func_name == "dot" and module_name == "np":
                # Suggest using np.matmul() instead
                self.add_message("numpy-dot-usage", node=node, confidence=HIGH)
