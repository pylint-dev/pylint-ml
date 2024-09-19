# Licensed under the MIT: https://mit-license.org/
# For details: https://github.com/pylint-dev/pylint-ml/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint-ml/CONTRIBUTORS.txt

"""Check for proper usage of Pandas functions with required parameters."""

from astroid import nodes
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

from pylint_ml.util.common import get_method_name
from pylint_ml.util.config import LIB_PANDAS
from pylint_ml.util.library_base_checker import LibraryBaseChecker


class PandasParameterChecker(LibraryBaseChecker):
    name = "pandas-parameter"
    msgs = {
        "W8111": (
            "Ensure that required parameters %s are explicitly specified in Pandas method %s.",
            "pandas-parameter",
            "Explicitly specifying required parameters improves model performance and prevents unintended behavior.",
        ),
    }

    # Define required parameters for specific Pandas classes and methods
    REQUIRED_PARAMS = {
        # DataFrame creation
        "DataFrame": ["data"],  # The primary input data for DataFrame creation
        # Concatenation
        "concat": ["objs"],  # The list or dictionary of DataFrames/Series to concatenate
        # DataFrame I/O (Input/Output)
        "read_csv": ["filepath_or_buffer", "dtype"],  # Path to CSV file or file-like object; column data types
        "read_excel": ["io", "dtype"],  # Path to Excel file or file-like object; column data types
        "read_table": ["filepath_or_buffer", "dtype"],  # Path to delimited text-file or file object; column data types
        "to_csv": ["path_or_buf"],  # File path or buffer to write the DataFrame to
        "to_excel": ["excel_writer"],  # File path or ExcelWriter object to write the data to
        # Merging and Joining
        "merge": ["right", "how", "on", "validate"],  # The DataFrame or Serie to merge with
        "join": ["other"],  # The DataFrame or Series to join
        # DataFrame Operations
        "pivot_table": ["index"],  # The column to pivot on (values and columns have defaults)
        "groupby": ["by"],  # The key or list of keys to group by
        "resample": ["rule"],  # The frequency rule to resample by
        # Data Cleaning and Transformation
        "fillna": ["value"],  # Value to use to fill NA/NaN values
        "drop": ["labels"],  # Labels to drop
        "drop_duplicates": ["subset"],  # Subset of columns to consider when dropping duplicates
        "replace": ["to_replace"],  # Values to replace
        # Plotting
        "plot": ["x"],  # x-values or index for plotting
        "hist": ["column"],  # Column to plot the histogram for
        "boxplot": ["column"],  # Column(s) to plot boxplot for
        # DataFrame Sorting
        "sort_values": ["by"],  # Column(s) to sort by
        "sort_index": ["axis"],  # Axis to sort along (index=0, columns=1)
        # Statistical Functions
        "corr": ["method"],  # Method to use for correlation ('pearson', 'kendall', 'spearman')
        "describe": [],  # No required parameters, but additional ones could be specified
        # Windowing/Resampling Functions
        "rolling": ["window"],  # Size of the moving window
        "ewm": ["span"],  # Span for exponentially weighted calculations
        # Miscellaneous Functions
        "apply": ["func"],  # Function to apply to the data
        "agg": ["func"],  # Function or list of functions for aggregation
    }

    @only_required_for_messages("pandas-parameter")
    def visit_call(self, node: nodes.Call) -> None:
        if not self.is_library_imported_and_version_valid(lib_name=LIB_PANDAS, required_version=None):
            return

        method_name = get_method_name(node)
        if method_name in self.REQUIRED_PARAMS:
            provided_keywords = {kw.arg for kw in node.keywords if kw.arg is not None}
            missing_params = [param for param in self.REQUIRED_PARAMS[method_name] if param not in provided_keywords]
            if missing_params:
                self.add_message(
                    "pandas-parameter",
                    node=node,
                    confidence=HIGH,
                    args=(", ".join(missing_params), method_name),
                )
