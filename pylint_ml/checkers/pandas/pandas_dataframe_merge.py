# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for proper usage of pandas merge() with explicit parameters and DataFrame naming conventions."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class PandasDataframeMergeChecker(BaseChecker):
    name = "pandas-dataframe-merge"
    msgs = {
        "W8110": (
            "Ensure that 'how', 'on', and 'validate' parameters are explicitly specified in pandas DataFrame merge().",
            "pandas-dataframe-merge",
            "Explicitly specifying the 'how', 'on', and 'validate' parameters and using a proper DataFrame naming "
            "convention improves readability and prevents unintended behavior.",
        ),
    }

    @only_required_for_messages("pandas-dataframe-merge")
    def visit_call(self, node: nodes.Call) -> None:
        if isinstance(node.func, nodes.Attribute):
            method_name = node.func.attrname
            object_name = getattr(node.func.expr, "name", "")
            if method_name == "merge":
                # Check if the DataFrame name starts with 'df_'
                name_is_valid = object_name.startswith("df_")

                # Check for explicit 'how', 'on', and 'validate' parameters
                how_specified = any(kw.arg == "how" for kw in node.keywords)
                on_specified = any(kw.arg == "on" for kw in node.keywords)
                validate_specified = any(kw.arg == "validate" for kw in node.keywords)

                if not (name_is_valid and how_specified and on_specified and validate_specified):
                    self.add_message("pandas-dataframe-merge", node=node, confidence=HIGH)
