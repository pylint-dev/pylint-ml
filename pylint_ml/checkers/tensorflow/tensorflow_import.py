# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for import of tensorflow library."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class TensorflowImportChecker(BaseChecker):
    name = "tensorflow-import"
    msgs = {
        "W8401": (
            "Tensorflow imported with incorrect alias",
            "tensorflow-import",
            "Tensorflow should be imported with the alias `tf` to maintain consistency with common practices. "
            "Importing Tensorflow with any other alias can lead to confusion. "
            "Consider using `import tensorflow as tf` for clarity and adherence to the convention.",
        ),
        "W8402": (
            "Direct import from Tensorflow discouraged",
            "tensorflow-importfrom",
            "Direct imports from Tensorflow using `from tensorflow import ...` are discouraged to maintain code "
            "clarity and prevent potential conflicts. Tensorflow should be imported with the alias `tf` following "
            "common practices. Using any other alias or direct import method can lead to confusion. "
            "Consider using `import tensorflow as tf` to adhere to the convention and ensure consistency.",
        ),
    }

    @only_required_for_messages("tensorflow-import")
    def visit_import(self, node: nodes.Import) -> None:
        for name, alias in node.names:
            if name == "tensorflow" and alias != "tf":
                self.add_message("tensorflow-import", node=node, confidence=HIGH)

    @only_required_for_messages("tensorflow-importfrom")
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        if node.modname == "tensorflow":
            self.add_message("tensorflow-importfrom", node=node, confidence=HIGH)
