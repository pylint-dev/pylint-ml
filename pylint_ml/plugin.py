"""pylint_ml plugin module."""

from pylint.lint import PyLinter

from pylint_ml.checkers.numpy.import_numpy import NumpyImportChecker
from pylint_ml.checkers.pandas.import_pandas import PandasImportChecker


def register(linter: PyLinter) -> None:
    """Register checkers."""
    # Numpy
    linter.register_checker(NumpyImportChecker(linter))

    # Pandas
    linter.register_checker(PandasImportChecker(linter))
