# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for import of scipy library."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class ScipyImportChecker(BaseChecker):
    name = "scipy-import"
    msgs = {
        "W8401": (
            "Direct or aliased Scipy import detected",
            "scipy-direct-aliased-import",
            "Using `import scipy` or `import scipy as ...` is not recommended. For better clarity and consistency, "
            "it is advisable to import specific submodules directly, using the `from scipy import ...` syntax. "
            "This approach prevents confusion and aligns with common practices by explicitly stating which "
            "components of Scipy are being used.",
        ),
    }

    @only_required_for_messages("scipy-import")
    def visit_import(self, node: nodes.Import) -> None:
        for name, _ in node.names:
            if name == "scipy":
                self.add_message("scipy-import", node=node, confidence=HIGH)
