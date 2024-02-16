# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for import of torch library."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class TorchImportChecker(BaseChecker):
    name = "torch-import"
    msgs = {
        "W8401": (
            "Torch imported with alias",
            "torch-import",
            "Torch should be imported without an alias to maintain consistency with common practices. "
            "Importing Torch with an alias can lead to confusion. "
            "Consider using `import torch` for clarity and adherence to the convention.",
        ),
        "W8402": (
            "Direct import from Torch discouraged",
            "torch-importfrom",
            "Direct imports from Torch using `from torch import ...` are discouraged to maintain code "
            "clarity and prevent potential conflicts. Using any alias or direct import method can lead to confusion. "
            "Consider using `import torch` to adhere to the convention and ensure consistency.",
        ),
    }

    @only_required_for_messages("torch-import")
    def visit_import(self, node: nodes.Import) -> None:
        for name, alias in node.names:
            if name == "torch" and alias:  # Alias is used
                self.add_message("torch-import", node=node, confidence=HIGH)

    @only_required_for_messages("torch-importfrom")
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        if node.modname == "torch":
            self.add_message("torch-importfrom", node=node, confidence=HIGH)
