import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.tensorflow.import_tensorflow import TensorflowImportChecker


class TestTensorflowImport(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = TensorflowImportChecker

    def test_correct_tensorflow_import(self):
        tensorflow_import_node = astroid.extract_node(
            """
        import tensorflow as tf
        """
        )

        with self.assertNoMessages():
            self.checker.visit_import(tensorflow_import_node)

    def test_incorrect_tensorflow_import(self):
        tensorflow_import_node = astroid.extract_node(
            """
        import tensorflow as tflow
        """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="tensorflow-import",
                confidence=HIGH,
                node=tensorflow_import_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(tensorflow_import_node)

    def test_incorrect_tensorflow_import_from(self):
        tensorflow_importfrom_node = astroid.extract_node(
            """
        from tensorflow import math
        """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="tensorflow-importfrom",
                confidence=HIGH,
                node=tensorflow_importfrom_node,
            ),
            ignore_position=True,
        ):
            self.checker.visit_importfrom(tensorflow_importfrom_node)
