import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.tensorflow.tensor_parameter import TensorFlowParameterChecker


class TestTensorParameterChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = TensorFlowParameterChecker

    def test_sequential_params(self):
        node = astroid.extract_node(
            """
            import tensorflow as tf
            model = tf.keras.models.Sequential()  # [tensor-parameter]
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
            self.checker.visit_call(sequential_call)

    def test_sequential_with_layers(self):
        node = astroid.extract_node(
            """
            import tensorflow as tf
            model = tf.keras.Sequential(layers=[
                tf.keras.layers.Dense(units=64, activation='relu'),
                tf.keras.layers.Dense(units=10)
            ])
            """
        )

        sequential_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(sequential_call)

    def test_compile_params(self):
        node = astroid.extract_node(
            """
            import tensorflow as tf
            model = tf.keras.models.Sequential()
            model.compile()  # [tensor-parameter]
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
            self.checker.visit_call(node)

    def test_compile_with_all_params(self):
        node = astroid.extract_node(
            """
            import tensorflow as tf
            model = tf.keras.models.Sequential()
            model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])  # No trigger
            """
        )

        compile_call = node

        with self.assertNoMessages():
            self.checker.visit_call(compile_call)

    def test_fit_params(self):
        node = astroid.extract_node(
            """
            import tensorflow as tf
            model = tf.keras.models.Sequential()
            model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
            model.fit(epochs=10)  # [tensor-parameter]
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
            self.checker.visit_call(fit_call)

    def test_fit_with_all_params(self):
        node = astroid.extract_node(
            """
            import tensorflow as tf
            model = tf.keras.models.Sequential()
            model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
            model.fit(x=train_data, y=train_labels, epochs=10)  # Should not trigger
            """
        )

        fit_call = node

        with self.assertNoMessages():
            self.checker.visit_call(fit_call)

    def test_conv2d_params(self):
        node = astroid.extract_node(
            """
            import tensorflow as tf
            layer = tf.keras.layers.Conv2D(kernel_size=(3, 3))  # [tensor-parameter]
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
            self.checker.visit_call(conv2d_call)

    def test_conv2d_with_all_params(self):
        node = astroid.extract_node(
            """
            import tensorflow as tf
            layer = tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3))  # Should not trigger
            """
        )

        conv2d_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(conv2d_call)

    def test_dense_params(self):
        node = astroid.extract_node(
            """
            import tensorflow as tf
            layer = tf.keras.layers.Dense()  # [tensor-parameter]
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
            self.checker.visit_call(dense_call)

    def test_dense_with_all_params(self):
        node = astroid.extract_node(
            """
            import tensorflow as tf
            layer = tf.keras.layers.Dense(units=64)  # Should not trigger
            """
        )

        dense_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(dense_call)
