# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for the usage of pandas.DataFrame.values and suggest .to_numpy() instead."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class PandasValuesChecker(BaseChecker):
    name = "pandas-dataframe-values"
    msgs = {
        "W8112": (
            "Avoid using 'DataFrame.values'. Use '.to_numpy()' instead for better consistency and compatibility.",
            "pandas-dataframe-values",
            "Using 'DataFrame.values' is discouraged as it may not always return a NumPy array. Use '.to_numpy()' "
            "instead.",
        ),
    }

    @only_required_for_messages("pandas-dataframe-values")
    def visit_attribute(self, node: nodes.Attribute) -> None:
        if isinstance(node.expr, nodes.Name):
            if node.attrname == "values" and node.expr.name.startswith("df_"):
                self.add_message("pandas-dataframe-values", node=node, confidence=HIGH)
