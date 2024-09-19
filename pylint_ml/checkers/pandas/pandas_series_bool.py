# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for usage of the deprecated pandas Series.bool() method."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

# Todo add version deprecated
from pylint_ml.util.config import LIB_PANDAS
from pylint_ml.util.library_base_checker import LibraryBaseChecker


class PandasSeriesBoolChecker(LibraryBaseChecker):
    name = "pandas-series-bool"
    msgs = {
        "W8105": (
            "Use of deprecated pandas Series.bool() method",
            "pandas-series-bool",
            "Avoid using the deprecated pandas Series.bool() method.",
        ),
    }

    @only_required_for_messages("pandas-series-bool")
    def visit_call(self, node: nodes.Call) -> None:
        if not self.is_library_imported_and_version_valid(lib_name=LIB_PANDAS, required_version=None):
            return

        if isinstance(node.func, nodes.Attribute):
            method_name = getattr(node.func, "attrname", None)

            if method_name == "bool":
                # Check if the object calling .bool() has a name starting with 'ser'
                object_name = getattr(node.func.expr, "name", None)
                if object_name and self._is_valid_series_name(object_name):
                    self.add_message("pandas-series-bool", node=node, confidence=HIGH)

    @staticmethod
    def _is_valid_series_name(name: str) -> bool:
        """Check if the Series name starts with 'ser_'."""
        return name.startswith("ser_")
