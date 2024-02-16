import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.torch.import_torch import TorchImportChecker


class TestTorchImport(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = TorchImportChecker

    def test_correct_torch_import(self):
        torch_import_node = astroid.extract_node(
            """
        import torch
        """
        )

        with self.assertNoMessages():
            self.checker.visit_import(torch_import_node)

    def test_incorrect_torch_import(self):
        torch_import_node = astroid.extract_node(
            """
        import torch as th
        """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="torch-import",
                confidence=HIGH,
                node=torch_import_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(torch_import_node)

    def test_incorrect_torch_import_from(self):
        torch_importfrom_node = astroid.extract_node(
            """
        from torch import min
        """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="torch-importfrom",
                confidence=HIGH,
                node=torch_importfrom_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_importfrom(torch_importfrom_node)
