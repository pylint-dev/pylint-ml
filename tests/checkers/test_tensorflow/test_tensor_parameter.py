from unittest.mock import patch

import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.tensorflow.tensor_parameter import TensorFlowParameterChecker


class TestTensorParameterChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = TensorFlowParameterChecker

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_sequential_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        import_node, node = astroid.extract_node(
            """
            import tensorflow as tf #@
            model = tf.keras.models.Sequential() #@
            """
        )

        sequential_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="tensor-parameter",
                confidence=HIGH,
                node=sequential_call,
                args=("layers", "Sequential"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_call(sequential_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_sequential_with_layers(self, mock_version):
        mock_version.return_value = "1.5.2"
        import_node, node = astroid.extract_node(
            """
            import tensorflow as tf #@
            model = tf.keras.Sequential(layers=[tf.keras.layers.Dense(units=64, activation='relu'),tf.keras.layers.Dense(units=10)]) #@
            """
        )

        sequential_call = node.value

        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_call(sequential_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_compile_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        import_node, node = astroid.extract_node(
            """
            import tensorflow as tf #@
            model = tf.keras.models.Sequential()
            model.compile() #@
            """
        )

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="tensor-parameter",
                confidence=HIGH,
                node=node,
                args=("optimizer, loss", "compile"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_call(node)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_compile_with_all_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        import_node, node = astroid.extract_node(
            """
            import tensorflow as tf #@
            model = tf.keras.models.Sequential()
            model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy']) #@
            """
        )

        compile_call = node

        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_call(compile_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_fit_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        import_node, node = astroid.extract_node(
            """
            import tensorflow as tf #@
            model = tf.keras.models.Sequential()
            model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
            model.fit(epochs=10) #@
            """
        )

        fit_call = node

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="tensor-parameter",
                confidence=HIGH,
                node=fit_call,
                args=("x, y", "fit"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_call(fit_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_fit_with_all_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        import_node, node = astroid.extract_node(
            """
            import tensorflow as tf #@
            model = tf.keras.models.Sequential()
            model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
            model.fit(x=train_data, y=train_labels, epochs=10) #@
            """
        )

        fit_call = node

        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_call(fit_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_conv2d_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        import_node, node = astroid.extract_node(
            """
            import tensorflow as tf #@
            layer = tf.keras.layers.Conv2D(kernel_size=(3, 3)) #@
            """
        )

        conv2d_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="tensor-parameter",
                confidence=HIGH,
                node=conv2d_call,
                args=("filters", "Conv2D"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_call(conv2d_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_conv2d_with_all_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        import_node, node = astroid.extract_node(
            """
            import tensorflow as tf #@
            layer = tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3)) #@
            """
        )

        conv2d_call = node.value

        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_call(conv2d_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_dense_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        import_node, node = astroid.extract_node(
            """
            import tensorflow as tf #@
            layer = tf.keras.layers.Dense() #@
            """
        )

        dense_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="tensor-parameter",
                confidence=HIGH,
                node=dense_call,
                args=("units", "Dense"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_import(import_node)
            self.checker.visit_call(dense_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_dense_with_all_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        import_node, node = astroid.extract_node(
            """
            import tensorflow as tf #@
            layer = tf.keras.layers.Dense(units=64) #@
            """
        )

        dense_call = node.value

        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_call(dense_call)
