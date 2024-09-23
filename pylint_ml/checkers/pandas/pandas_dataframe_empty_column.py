# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for proper initialization of empty columns in pandas DataFrames."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

from pylint_ml.checkers.config import PANDAS
from pylint_ml.checkers.library_base_checker import LibraryBaseChecker


class PandasEmptyColumnChecker(LibraryBaseChecker):
    name = "pandas-dataframe-empty-column"
    msgs = {
        "W8113": (
            "Avoid using filler values (0, '') for new empty columns. Use 'np.nan' or 'pd.Series(dtype=...)' instead.",
            "pandas-dataframe-empty-column",
            "Initializing new columns with filler values such as 0 or empty strings can lead to issues with null "
            "value detection.",
        ),
    }

    @only_required_for_messages("pandas-dataframe-empty-column")
    def visit_subscript(self, node: nodes.Subscript) -> None:
        if not self.is_library_imported_and_version_valid(lib_name=PANDAS, required_version=None):
            return

        if isinstance(node.value, nodes.Name) and node.value.name.startswith("df_"):
            if isinstance(node.slice, nodes.Const) and isinstance(node.parent, nodes.Assign):
                if isinstance(node.parent.value, nodes.Const):
                    # Checking for filler values: 0 or empty string
                    if node.parent.value.value in (0, ""):
                        self.add_message("pandas-dataframe-empty-column", node=node, confidence=HIGH)
