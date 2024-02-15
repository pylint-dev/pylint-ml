# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for import of pandas library."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class PandasImportChecker(BaseChecker):
    name = "pandas-import"
    msgs = {
        "W8101": (
            "Pandas imported with incorrect alias",
            "pandas-import",
            "Pandas should be imported with the alias `pd` to maintain consistency with common practices. "
            "Importing pandas with any other alias can lead to confusion. "
            "Consider using `import pandas as pd` for clarity and adherence to the convention.",
        ),
        "W8102": (
            "Direct import from Pandas discouraged",
            "pandas-importfrom",
            "Direct imports from Pandas using `from pandas import ...` are discouraged to maintain code clarity and "
            "prevent potential conflicts. Pandas should be imported with the alias `pd` following common practices. "
            "Using any other alias or direct import method can lead to confusion. "
            "Consider using `import pandas as pd` to adhere to the convention and ensure consistency.",
        ),
    }

    @only_required_for_messages("pandas-import")
    def visit_import(self, node: nodes.Import) -> None:
        for name, alias in node.names:
            if name == "pandas" and alias != "pd":
                self.add_message("pandas-import", node=node, confidence=HIGH)

    @only_required_for_messages("pandas-importfrom")
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        if node.modname == "pandas":
            self.add_message("pandas-importfrom", node=node, confidence=HIGH)
