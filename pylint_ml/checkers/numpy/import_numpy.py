# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for import of numpy library."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class NumpyImportChecker(BaseChecker):
    name = "numpy-import"
    msgs = {
        "W8001": (
            "Numpy imported with incorrect alias",
            "numpy-import",
            "Numpy should be imported with the alias `np` to maintain consistency with common practices. "
            "Importing numpy with any other alias can lead to confusion. "
            "Consider using `import numpy as np` for clarity and adherence to the convention.",
        ),
        "W8002": (
            "Direct import from Numpy discouraged",
            "numpy-importfrom",
            "Direct imports from Numpy using `from numpy import ...` are discouraged to maintain code clarity and "
            "prevent potential conflicts. Numpy should be imported with the alias `np` following common practices. "
            "Using any other alias or direct import method can lead to confusion. "
            "Consider using `import numpy as np` to adhere to the convention and ensure consistency.",
        ),
    }

    @only_required_for_messages("numpy-import")
    def visit_import(self, node: nodes.Import) -> None:
        for name, alias in node.names:
            if name == "numpy" and alias != "np":
                self.add_message("numpy-import", node=node, confidence=HIGH)

    @only_required_for_messages("numpy-importfrom")
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        if node.modname == "numpy":
            self.add_message("numpy-importfrom", node=node, confidence=HIGH)
