# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for proper usage of PyTorch functions with required parameters."""

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

from pylint_ml.util.config import LIB_TENSORFLOW
from pylint_ml.util.library_base_checker import LibraryBaseChecker


class PyTorchParameterChecker(LibraryBaseChecker):
    name = "pytorch-parameter"
    msgs = {
        "W8111": (
            "Ensure that required parameters %s are explicitly specified in PyTorch method %s.",
            "pytorch-parameter",
            "Explicitly specifying required parameters improves model performance and prevents unintended behavior.",
        ),
    }

    # Define required parameters for specific PyTorch methods
    REQUIRED_PARAMS = {
        # Optimizers
        "SGD": ["lr"],  # Focus on the critical learning rate parameter
        "Adam": ["lr"],  # Learning rate is typically the most important for tuning
        # Layers
        "Conv2d": ["in_channels", "out_channels", "kernel_size"],
        # These parameters define the convolution's core operation
        "Linear": ["in_features", "out_features"],  # Essential to define the transformation dimensions
        "LSTM": ["input_size", "hidden_size"],  # Essential for defining the dimensionality of the LSTM cell
    }

    @only_required_for_messages("pytorch-parameter")
    def visit_call(self, node: nodes.Call) -> None:
        if not self.is_library_imported_and_version_valid(lib_name=LIB_TENSORFLOW, required_version=None):
            return

        method_name = self._get_method_name(node)
        if method_name in self.REQUIRED_PARAMS:
            provided_keywords = {kw.arg for kw in node.keywords if kw.arg is not None}
            # Collect all missing parameters
            missing_params = [param for param in self.REQUIRED_PARAMS[method_name] if param not in provided_keywords]
            if missing_params:
                self.add_message(
                    "pytorch-parameter",
                    node=node,
                    confidence=HIGH,
                    args=(", ".join(missing_params), method_name),
                )

    @staticmethod
    def _get_method_name(node: nodes.Call) -> str:
        """Extracts the method name from a Call node, including handling chained calls."""
        func = node.func
        while isinstance(func, nodes.Attribute):
            func = func.expr
        return (
            node.func.attrname
            if isinstance(node.func, nodes.Attribute)
            else func.name if isinstance(func, nodes.Name) else ""
        )
