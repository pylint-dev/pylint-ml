"""pylint_ml plugin module."""

from pylint.lint import PyLinter

from pylint_ml.checkers.numpy.numpy_import import NumpyImportChecker
from pylint_ml.checkers.numpy.numpy_nan_comparison import NumpyNaNComparisonChecker
from pylint_ml.checkers.pandas.pandas_import import PandasImportChecker
from pylint_ml.checkers.scipy.scipy_import import ScipyImportChecker
from pylint_ml.checkers.sklearn.sklearn_import import SklearnImportChecker
from pylint_ml.checkers.tensorflow.tensorflow_import import TensorflowImportChecker
from pylint_ml.checkers.torch.torch_parameter import PyTorchParameterChecker


def register(linter: PyLinter) -> None:
    """Register checkers."""
    # Numpy
    linter.register_checker(NumpyImportChecker(linter))
    linter.register_checker(NumpyNaNComparisonChecker(linter))

    # Pandas
    linter.register_checker(PandasImportChecker(linter))

    # Tensorflow
    linter.register_checker(TensorflowImportChecker(linter))

    # Torch
    linter.register_checker(PyTorchParameterChecker(linter))

    # Scipy
    linter.register_checker(ScipyImportChecker(linter))

    # Sklearn
    linter.register_checker(SklearnImportChecker(linter))

    # Theano
    # Matplotlib
