# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for the usage of pandas.DataFrame.values and suggest .to_numpy() instead."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers.utils import only_required_for_messages, safe_infer
from pylint.interfaces import HIGH

from pylint_ml.checkers.config import PANDAS
from pylint_ml.checkers.library_base_checker import LibraryBaseChecker


class PandasValuesChecker(LibraryBaseChecker):
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
        if not self.is_library_imported_and_version_valid(lib_name=PANDAS, required_version=None):
            return

        if isinstance(node.expr, nodes.Name):
            if (
                node.attrname == "values"
                and node.expr.name.startswith("df_")
                and PANDAS in safe_infer(node.expr).qname()
            ):
                self.add_message("pandas-dataframe-values", node=node, confidence=HIGH)
