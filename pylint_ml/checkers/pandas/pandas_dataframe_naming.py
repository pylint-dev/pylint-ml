# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for consistent naming of pandas DataFrame variables."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class PandasDataFrameNamingChecker(BaseChecker):
    name = "pandas-dataframe-naming"
    msgs = {
        "W8103": (
            "Pandas DataFrame variable names should start with 'df_' followed by descriptive text",
            "pandas-dataframe-naming",
            "Ensure that pandas DataFrame variables follow the naming convention.",
        ),
    }

    @only_required_for_messages("pandas-dataframe-naming")
    def visit_assign(self, node: nodes.Assign) -> None:
        if isinstance(node.value, nodes.Call):
            func_name = getattr(node.value.func, "attrname", None)
            module_name = getattr(node.value.func.expr, "name", None)

            if func_name == "DataFrame" and module_name == "pd":
                for target in node.targets:
                    if isinstance(target, nodes.AssignName):
                        var_name = target.name
                        if not var_name.startswith("df_") or len(var_name) <= 3:
                            self.add_message("pandas-dataframe-naming", node=node, confidence=HIGH)
