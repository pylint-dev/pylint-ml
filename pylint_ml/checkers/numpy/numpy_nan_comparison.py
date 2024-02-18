# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for numpy nan comparison."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

COMPARISON_OP = frozenset(("<", "<=", ">", ">=", "!=", "=="))
NUMPY_NAN = frozenset(("nan", "NaN", "NAN"))


class NumpyNaNComparisonChecker(BaseChecker):
    name = "numpy-nan-compare"
    msgs = {
        "W8001": (
            "Numpy nan comparison used",
            "numpy-nan-compare",
            "Since comparing NaN with NaN always returns False, use np.isnan() to check for NaN values.",
        ),
    }

    @classmethod
    def __is_np_nan_call(cls, node):
        """Check if the node represents a call to np.nan."""
        return (
            isinstance(node, nodes.Call)
            and isinstance(node.func, nodes.Attribute)
            and node.func.attrname in NUMPY_NAN
            and isinstance(node.func.expr, nodes.Name)
            and node.func.expr.name == "np"
        )

    @only_required_for_messages("numpy-nan-compare")
    def visit_compare(self, node: nodes.Compare) -> None:
        # Why am I getting node: node.Call here? Should be nodes.Compare...
        # Check test case test_numpy/test_numpy_nan_comparison.py
        if self.__is_np_nan_call(node.left):
            self.add_message("numpy-nan-compare", node=node, confidence=HIGH)
            return

        for op, comparator in node.ops:
            if op in COMPARISON_OP and self.__is_np_nan_call(comparator):
                self.add_message("numpy-nan-compare", node=node, confidence=HIGH)
                return
