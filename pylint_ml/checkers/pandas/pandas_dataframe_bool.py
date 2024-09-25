# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for usage of the deprecated pandas DataFrame.bool() method."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

from pylint_ml.checkers.config import PANDAS
from pylint_ml.checkers.library_base_checker import LibraryBaseChecker
from pylint_ml.checkers.utils import infer_specific_module_from_call


class PandasDataFrameBoolChecker(LibraryBaseChecker):
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
        if not self.is_library_imported_and_version_valid(lib_name=PANDAS, required_version="2.1.0"):
            return

        if isinstance(node.func, nodes.Attribute):
            method_name = getattr(node.func, "attrname", None)
            if method_name == "bool":
                # Check if the object calling .bool() has a name starting with 'df_'
                object_name = getattr(node.func.expr, "name", None)
                if (
                    infer_specific_module_from_call(node=node, module_name=PANDAS)
                    and object_name
                    and self._is_valid_dataframe_name(object_name)
                ):
                    self.add_message("pandas-dataframe-bool", node=node, confidence=HIGH)

    @staticmethod
    def _is_valid_dataframe_name(name: str) -> bool:
        """Check if the DataFrame name starts with 'df_'."""
        return name.startswith("df_")
