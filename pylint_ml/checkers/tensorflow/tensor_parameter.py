# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for proper usage of Tensorflow functions with required parameters."""

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class TensorFlowParameterChecker(BaseChecker):
    name = "tensor-parameter"
    msgs = {
        "W8111": (
            "Ensure that required parameters %s are explicitly specified in TensorFlow method %s.",
            "tensor-parameter",
            "Explicitly specifying required parameters improves model performance and prevents unintended behavior.",
        ),
    }

    # Define required parameters for specific TensorFlow methods
    REQUIRED_PARAMS = {
        # Model Creation
        "Sequential": ["layers"],  # Layers must be specified to build a model
        # Model Compilation
        "compile": ["optimizer", "loss"],  # Optimizer and loss function are essential for training
        # Model Training
        "fit": ["x", "y"],  # Input data (x) and target data (y) are required to train the model
        # Layers
        "Conv2D": ["filters", "kernel_size"],  # Filters and kernel size define the convolutional layer's structure
        "Dense": ["units"],  # Number of units (neurons) is crucial for a Dense layer
    }

    @only_required_for_messages("tensor-parameter")
    def visit_call(self, node: nodes.Call) -> None:
        method_name = self._get_method_name(node)
        if method_name in self.REQUIRED_PARAMS:
            provided_keywords = {kw.arg for kw in node.keywords if kw.arg is not None}
            # Collect all missing parameters
            missing_params = [param for param in self.REQUIRED_PARAMS[method_name] if param not in provided_keywords]
            if missing_params:
                self.add_message(
                    "tensor-parameter",
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
