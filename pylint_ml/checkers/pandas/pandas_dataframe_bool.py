# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for usage of the deprecated pandas DataFrame.bool() method."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class PandasDataFrameBoolChecker(BaseChecker):
    name = "pandas-dataframe-bool"
    msgs = {
        "W8104": (
            "Use of deprecated pandas DataFrame.bool() method",
            "pandas-dataframe-bool",
            "Avoid using the deprecated pandas DataFrame.bool() method.",
        ),
    }

    @only_required_for_messages("pandas-dataframe-bool")
    def visit_call(self, node: nodes.Call) -> None:
        if isinstance(node.func, nodes.Attribute):
            method_name = getattr(node.func, "attrname", None)
            module_name = getattr(node.func.expr, "name", None)

            if method_name == "bool" and module_name == "pd":
                self.add_message("pandas-dataframe-bool", node=node, confidence=HIGH)

    def _check_method_usage(self, node):
        method_name = getattr(node.func, "attrname", None)
        module_name = getattr(node.func.expr, "name", None)
        if method_name == "bool" and module_name == "pd":
            self.add_message("pandas-dataframe-bool", node=node, confidence=HIGH)
