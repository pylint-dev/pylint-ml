# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for using dictionary-like column selection over property-like selection in pandas DataFrames."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class PandasColumnSelectionChecker(BaseChecker):
    name = "pandas-column-selection"
    msgs = {
        "W8118": (
            "Use dictionary-like column selection (df['column']) instead of property-like selection (df.column).",
            "pandas-column-selection",
            "Ensure that pandas DataFrame columns are selected using dictionary-like syntax for clarity and safety.",
        ),
    }

    @only_required_for_messages("pandas-column-selection")
    def visit_attribute(self, node: nodes.Attribute) -> None:
        """Check for attribute access that might be a column selection."""
        if isinstance(node.expr, nodes.Name) and node.expr.name.startswith("df_"):
            # Issue a warning for property-like access
            self.add_message("pandas-column-selection", node=node, confidence=HIGH)
