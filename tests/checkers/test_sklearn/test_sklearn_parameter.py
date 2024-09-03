import astroid
import pylint.testutils
from pylint.interfaces import HIGH

from pylint_ml.checkers.sklearn.sklearn_parameter import SklearnParameterChecker


class TestSklearnParameterChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = SklearnParameterChecker

    def test_random_forest_params(self):
        node = astroid.extract_node(
            """
            from sklearn.ensemble import RandomForestClassifier
            clf = RandomForestClassifier()  # [sklearn-parameter]
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

    def test_random_forest_with_params(self):
        node = astroid.extract_node(
            """
            from sklearn.ensemble import RandomForestClassifier
            clf = RandomForestClassifier(n_estimators=100)  # Should not trigger
            """
        )

        forest_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(forest_call)

    def test_svc_params(self):
        node = astroid.extract_node(
            """
            from sklearn.svm import SVC
            clf = SVC()  # [sklearn-parameter]
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

    def test_svc_with_params(self):
        node = astroid.extract_node(
            """
            from sklearn.svm import SVC
            clf = SVC(C=1.0, kernel='linear')  # Should not trigger
            """
        )

        svc_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(svc_call)

    def test_kmeans_params(self):
        node = astroid.extract_node(
            """
            from sklearn.cluster import KMeans
            kmeans = KMeans()  # [sklearn-parameter]
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

    def test_kmeans_with_params(self):
        node = astroid.extract_node(
            """
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=8)  # Should not trigger
            """
        )

        kmeans_call = node.value

        with self.assertNoMessages():
            self.checker.visit_call(kmeans_call)
