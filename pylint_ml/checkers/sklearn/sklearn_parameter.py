# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for proper usage of Scikit-learn functions with required parameters."""

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class SklearnParameterChecker(BaseChecker):
    name = "sklearn-parameter"
    msgs = {
        "W8111": (
            "Ensure that required parameters %s are explicitly specified in Sklearn method %s.",
            "sklearn-parameter",
            "Explicitly specifying required parameters improves model performance and prevents unintended behavior.",
        ),
    }

    # Define required parameters for specific scikit-learn classes and methods
    REQUIRED_PARAMS = {
        # Model Creation and Initialization
        "RandomForestClassifier": ["n_estimators"],  # Number of trees in the forest is crucial
        "SVC": ["C", "kernel"],  # Regularization parameter and kernel type are essential
        "LogisticRegression": ["penalty", "C"],  # Regularization penalty and strength are critical
        "KMeans": ["n_clusters"],  # Number of clusters to form is a core parameter
        # Model Training
        "fit": ["X", "y"],  # Input data (X) and target labels (y) are required for training
        # Cross-Validation
        "cross_val_score": ["estimator", "X"],  # Estimator and input data are essential for cross-validation
        # Grid Search
        "GridSearchCV": ["estimator", "param_grid"],  # Estimator and parameter grid are crucial for grid search
    }

    @only_required_for_messages("sklearn-parameter")
    def visit_call(self, node: nodes.Call) -> None:
        method_name = self._get_method_name(node)
        if method_name in self.REQUIRED_PARAMS:
            provided_keywords = {kw.arg for kw in node.keywords if kw.arg is not None}
            # Collect all missing parameters
            missing_params = [param for param in self.REQUIRED_PARAMS[method_name] if param not in provided_keywords]
            if missing_params:
                self.add_message(
                    "sklearn-parameter",
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
