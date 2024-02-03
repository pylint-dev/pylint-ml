# Inside hello_plugin.py
from typing import TYPE_CHECKING

import astroid

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def register(linter: "PyLinter") -> None:
  """This required method auto registers the checker during initialization.

  :param linter: The linter to register the checker to.
  """
  print('Hello world')