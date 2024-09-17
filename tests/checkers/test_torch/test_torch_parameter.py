import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.torch.torch_parameter import PyTorchParameterChecker


class TestTorchParameterChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = PyTorchParameterChecker

    def test_sgd_params(self):
        node = astroid.extract_node(
            """
            import torch.optim as optim
            optimizer = optim.SGD(model.parameters(), momentum=0.9)  #@
            """
        )

        sgd_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pytorch-parameter",
                confidence=HIGH,
                node=sgd_call,
                args=("lr", "SGD"),  # Specify the expected missing parameters and method name
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(sgd_call)

    def test_sgd_with_all_params(self):
        node = astroid.extract_node(
            """
            import torch.optim as optim
            optimizer = optim.SGD(lr=0.01)  #@
            """
        )

        sgd_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(sgd_call)

    def test_adam_params(self):
        node = astroid.extract_node(
            """
            import torch.optim as optim
            optimizer = optim.Adam(model.parameters())  #@
            """
        )

        adam_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pytorch-parameter",
                confidence=HIGH,
                node=adam_call,
                args=("lr", "Adam"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(adam_call)

    def test_adam_with_all_params(self):
        node = astroid.extract_node(
            """
            import torch.optim as optim
            optimizer = optim.Adam(lr=0.001)  #@
            """
        )

        adam_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(adam_call)

    def test_conv2d_params(self):
        node = astroid.extract_node(
            """
            import torch.nn as nn
            layer = nn.Conv2d(in_channels=3, kernel_size=3)  #@
            """
        )

        conv2d_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pytorch-parameter",
                confidence=HIGH,
                node=conv2d_call,
                args=("out_channels", "Conv2d"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(conv2d_call)

    def test_conv2d_with_all_params(self):
        node = astroid.extract_node(
            """
            import torch.nn as nn
            layer = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3)  #@
            """
        )

        conv2d_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(conv2d_call)

    def test_linear_params(self):
        node = astroid.extract_node(
            """
            import torch.nn as nn
            layer = nn.Linear(in_features=128)  #@
            """
        )

        linear_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pytorch-parameter",
                confidence=HIGH,
                node=linear_call,
                args=("out_features", "Linear"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(linear_call)

    def test_linear_with_all_params(self):
        node = astroid.extract_node(
            """
            import torch.nn as nn
            layer = nn.Linear(in_features=128, out_features=64)  #@
            """
        )

        linear_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(linear_call)

    def test_lstm_params(self):
        node = astroid.extract_node(
            """
            import torch.nn as nn
            layer = nn.LSTM(input_size=128)  #@
            """
        )

        lstm_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="pytorch-parameter",
                confidence=HIGH,
                node=lstm_call,
                args=("hidden_size", "LSTM"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(lstm_call)

    def test_lstm_with_all_params(self):
        node = astroid.extract_node(
            """
            import torch.nn as nn
            layer = nn.LSTM(input_size=128, hidden_size=64)  #@
            """
        )

        lstm_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(lstm_call)
