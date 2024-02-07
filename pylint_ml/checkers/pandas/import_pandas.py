# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for import of pandas library."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class PandasImportChecker(BaseChecker):
    name = "pandas_import"
    msgs = {
        "W8020": (
            "Pandas imported with incorrect alias",
            "pandas-imported-incorrectly",
            "Pandas should be imported with the alias `pd` to maintain consistency with common practices. "
            "Importing pandas with any other alias can lead to confusion. "
            "Consider using `import pandas as pd` for clarity and adherence to the convention.",
        )
    }

    @only_required_for_messages("pandas_import")
    def visit_import(self, node: nodes.Import) -> None:
        for name, alias in node.names:
            if name == "pandas" and alias != "pd":
                self.add_message("pandas_import", node=node)


def register(linter: PyLinter) -> None:
    linter.register_checker(PandasImportChecker(linter))
