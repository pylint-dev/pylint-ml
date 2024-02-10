# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for import of numpy library."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages


class NumpyImportChecker(BaseChecker):
    name = "numpy_import"
    msgs = {
        "W8010": (
            "Numpy imported with incorrect alias",
            "numpy-imported-incorrectly",
            "Numpy should be imported with the alias `np` to maintain consistency with common practices. "
            "Importing numpy with any other alias can lead to confusion. "
            "Consider using `import numpy as np` for clarity and adherence to the convention.",
        )
    }

    @only_required_for_messages("numpy_import")
    def visit_import(self, node: nodes.Import) -> None:
        for name, alias in node.names:
            if name == "numpy" and alias != "np":
                self.add_message("numpy_import", node=node)
