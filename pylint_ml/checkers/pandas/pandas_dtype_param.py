from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH


class PandasDtypeChecker(BaseChecker):
    name = "pandas-dtype-param"
    msgs = {
        "W8117": (
            "Specify 'dtype' when using '%s' for better performance and data integrity.",
            "pandas-dtype-param",
            "It's recommended to explicitly specify the 'dtype' parameter in pandas read functions.",
        ),
    }

    @only_required_for_messages("pandas-dtype-param")
    def visit_call(self, node: nodes.Call) -> None:
        # Check if the function being called is a pandas read function
        if isinstance(node.func, nodes.Attribute):
            module_name = getattr(node.func.expr, "name", None)
            func_name = node.func.attrname

            if module_name == "pd" and func_name in {"read_csv", "read_excel", "read_table"}:
                # Check if dtype is specified
                if not any(kw.arg == "dtype" for kw in node.keywords):
                    self.add_message("pandas-dtype-param", node=node, confidence=HIGH)
