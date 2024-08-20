# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for improper usage of the inplace parameter in pandas operations."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class PandasInplaceChecker(BaseChecker):
    name = "pandas-inplace"
    msgs = {
        "W8109": (
            "Avoid using 'inplace=True' in pandas operations.",
            "pandas-inplace",
            "Using 'inplace=True' can lead to unclear and potentially problematic code. Prefer using assignment "
            "instead.",
        ),
    }

    _inplace_methods = {
        "drop",
        "fillna",
        "replace",
        "rename",
        "set_index",
        "reset_index",
        "sort_values",
        "sort_index",
        "drop_duplicates",
        "update",
        "clip",
    }

    @only_required_for_messages("pandas-inplace")
    def visit_call(self, node: nodes.Call) -> None:
        # Check if the call is to a method that supports 'inplace'
        if isinstance(node.func, nodes.Attribute):
            method_name = node.func.attrname
            if method_name in self._inplace_methods:
                for keyword in node.keywords:
                    if keyword.arg == "inplace" and getattr(keyword.value, "value", False) is True:
                        self.add_message("pandas-inplace", node=node, confidence=HIGH)
                        break
