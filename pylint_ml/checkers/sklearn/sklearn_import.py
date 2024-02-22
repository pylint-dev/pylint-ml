# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for import of sklearn library."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class SklearnImportChecker(BaseChecker):
    name = "sklearn-import"
    msgs = {
        "W8401": (
            "Direct or aliased Sklearn import detected",
            "sklearn-import",
            "Using `import sklearn` or `import sklearn as ...` is not recommended. For better clarity and consistency, "
            "it is advisable to import specific submodules directly, using the `from sklearn import ...` syntax. "
            "This approach prevents confusion and aligns with common practices by explicitly stating which "
            "components of Sklearn are being used.",
        ),
    }

    @only_required_for_messages("sklearn-import")
    def visit_import(self, node: nodes.Import) -> None:
        for name, _ in node.names:
            if name == "sklearn":
                self.add_message("sklearn-import", node=node, confidence=HIGH)
