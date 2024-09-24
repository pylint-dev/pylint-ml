from unittest.mock import patch

import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.sklearn.sklearn_parameter import SklearnParameterChecker


class TestSklearnParameterChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = SklearnParameterChecker

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_random_forest_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        node = astroid.extract_node(
            """
            from sklearn.ensemble import RandomForestClassifier
            clf = RandomForestClassifier()  #@
            """
        )

        forest_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="sklearn-parameter",
                confidence=HIGH,
                node=forest_call,
                args=("n_estimators", "RandomForestClassifier"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(forest_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_random_forest_with_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        node = astroid.extract_node(
            """
            from sklearn.ensemble import RandomForestClassifier
            clf = RandomForestClassifier(n_estimators=100)  #@
            """
        )

        forest_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(forest_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_svc_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        node = astroid.extract_node(
            """
            from sklearn.svm import SVC
            clf = SVC()  #@
            """
        )

        svc_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="sklearn-parameter",
                confidence=HIGH,
                node=svc_call,
                args=("C, kernel", "SVC"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(svc_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_svc_with_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        node = astroid.extract_node(
            """
            from sklearn.svm import SVC
            clf = SVC(C=1.0, kernel='linear')  #@
            """
        )

        svc_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(svc_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_kmeans_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        node = astroid.extract_node(
            """
            from sklearn.cluster import KMeans
            kmeans = KMeans()  #@
            """
        )

        kmeans_call = node.value

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="sklearn-parameter",
                confidence=HIGH,
                node=kmeans_call,
                args=("n_clusters", "KMeans"),
            ),
            ignore_position=True,
        ):
            self.checker.visit_call(kmeans_call)

    @patch("pylint_ml.checkers.library_base_checker.version")
    def test_kmeans_with_params(self, mock_version):
        mock_version.return_value = "1.5.2"
        node = astroid.extract_node(
            """
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=8)  #@
            """
        )

        kmeans_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(kmeans_call)
