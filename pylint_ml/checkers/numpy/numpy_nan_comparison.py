# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for numpy nan comparison."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

from pylint_ml.util.config import LIB_NUMPY
from pylint_ml.util.library_handler import LibraryBaseChecker

COMPARISON_OP = frozenset(("<", "<=", ">", ">=", "!=", "=="))
NUMPY_NAN = frozenset(("nan", "NaN", "NAN"))


class NumpyNaNComparisonChecker(LibraryBaseChecker):
    name = "numpy-nan-compare"
    msgs = {
        "W8001": (
            "Numpy nan comparison used",
            "numpy-nan-compare",
            "Since comparing NaN with NaN always returns False, use np.isnan() to check for NaN values.",
        ),
    }

    @classmethod
    def __is_np_nan_call(cls, node: nodes.Attribute) -> bool:
        """Check if the node represents a call to np.nan."""
        return node.attrname in NUMPY_NAN and isinstance(node.expr, nodes.Name) and node.expr.name == "np"

    @only_required_for_messages("numpy-nan-compare")
    def visit_compare(self, node: nodes.Compare) -> None:
        if not self.is_library_imported_and_version_valid(lib_name=LIB_NUMPY, required_version=None):
            return

        if isinstance(node.left, nodes.Attribute) and self.__is_np_nan_call(node.left):
            self.add_message("numpy-nan-compare", node=node, confidence=HIGH)
            return

        for op, comparator in node.ops:
            if op in COMPARISON_OP and isinstance(comparator, nodes.Attribute) and self.__is_np_nan_call(comparator):
                self.add_message("numpy-nan-compare", node=node, confidence=HIGH)
                return
