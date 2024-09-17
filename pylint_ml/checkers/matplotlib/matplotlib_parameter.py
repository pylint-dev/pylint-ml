# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for proper usage of Matplotlib functions with required parameters."""

from astroid import nodes
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

from pylint_ml.util.library_handler import LibraryHandler


class MatplotlibParameterChecker(LibraryHandler):
    name = "matplotlib-parameter"
    msgs = {
        "W8111": (
            "Ensure that required parameters %s are explicitly specified in matplotlib method %s.",
            "matplotlib-parameter",
            "Explicitly specifying required parameters improves model performance and prevents unintended behavior.",
        ),
    }

    # Define required parameters for specific matplotlib classes and methods
    REQUIRED_PARAMS = {
        # Plotting Functions
        "plot": ["x", "y"],  # x and y data points are required for basic line plots
        "scatter": ["x", "y"],  # x and y data points are required for scatter plots
        "bar": ["x", "height"],  # x positions and heights are required for bar plots
        "hist": ["x"],  # Data points (x) are required for histogram plots
        "pie": ["x"],  # x data is required for pie chart slices
        "imshow": ["X"],  # Input array (X) is required for displaying images
        "contour": ["X", "Y", "Z"],  # X, Y, and Z data points are required for contour plots
        "contourf": ["X", "Y", "Z"],  # X, Y, and Z data points for filled contour plots
        "pcolormesh": ["X", "Y", "C"],  # X, Y grid and C color values are required for pseudo color plot
        # Axes Functions
        "set_xlabel": ["xlabel"],  # xlabel is required for setting the x-axis label
        "set_ylabel": ["ylabel"],  # ylabel is required for setting the y-axis label
        "set_xlim": ["left", "right"],  # Left and right bounds for x-axis limit
        "set_ylim": ["bottom", "top"],  # Bottom and top bounds for y-axis limit
        # Figures and Subplots
        "subplots": ["nrows", "ncols"],  # Number of rows and columns are required for creating a subplot grid
        "subplot": ["nrows", "ncols", "index"],  # Number of rows, columns, and index for specific subplot
        # Miscellaneous Functions
        "savefig": ["fname"],  # Filename or file object is required to save a figure
    }

    @only_required_for_messages("matplotlib-parameter")
    def visit_call(self, node: nodes.Call) -> None:
        # TODO Update
        # if not self.is_library_imported('matplotlib') and self.is_library_version_valid(lib_version=):
        #     return

        method_name = self._get_full_method_name(node)
        if method_name in self.REQUIRED_PARAMS:
            provided_keywords = {kw.arg for kw in node.keywords if kw.arg is not None}
            missing_params = [param for param in self.REQUIRED_PARAMS[method_name] if param not in provided_keywords]
            if missing_params:
                self.add_message(
                    "matplotlib-parameter",
                    node=node,
                    confidence=HIGH,
                    args=(", ".join(missing_params), method_name),
                )

    def _get_full_method_name(self, node: nodes.Call) -> str:
        func = node.func
        method_chain = []

        while isinstance(func, nodes.Attribute):
            method_chain.insert(0, func.attrname)
            func = func.expr
        if isinstance(func, nodes.Name):
            method_chain.insert(0, func.name)

        return ".".join(method_chain)
