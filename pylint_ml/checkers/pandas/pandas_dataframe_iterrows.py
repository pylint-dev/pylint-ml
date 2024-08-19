# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for usage of the inefficient pandas DataFrame.iterrows() method."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class PandasIterrowsChecker(BaseChecker):
    name = "pandas-iterrows"
    msgs = {
        "W8106": (
            "Usage of pandas DataFrame.iterrows() detected",
            "pandas-iterrows",
            "Avoid using DataFrame.iterrows() for large datasets. Consider using vectorized operations or "
            ".itertuples() instead.",
        ),
    }

    @only_required_for_messages("pandas-iterrows")
    def visit_call(self, node: nodes.Call) -> None:
        if isinstance(node.func, nodes.Attribute):
            method_name = getattr(node.func, "attrname", None)
            if method_name == "iterrows":
                object_name = getattr(node.func.expr, "name", None)
                if object_name and self._is_dataframe_name(object_name):
                    self.add_message("pandas-iterrows", node=node, confidence=HIGH)

    @staticmethod
    def _is_dataframe_name(name: str) -> bool:
        """Check if the object name suggests it's a DataFrame (e.g., starts with 'df_')."""
        return name.startswith("df_")
