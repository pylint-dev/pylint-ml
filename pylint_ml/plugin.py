"""pylint_ml plugin module."""

from pylint.lint import PyLinter

from pylint_ml.checkers.numpy.import_numpy import NumpyImportChecker
from pylint_ml.checkers.pandas.import_pandas import PandasImportChecker
from pylint_ml.checkers.tensorflow.import_tensorflow import TensorflowImportChecker
from pylint_ml.checkers.torch.import_torch import TorchImportChecker


def register(linter: PyLinter) -> None:
    """Register checkers."""
    # Numpy
    linter.register_checker(NumpyImportChecker(linter))

    # Pandas
    linter.register_checker(PandasImportChecker(linter))

    # Tensorflow
    linter.register_checker(TensorflowImportChecker(linter))

    # Torch
    linter.register_checker(TorchImportChecker(linter))

    # Sklearn
    # Scipy
