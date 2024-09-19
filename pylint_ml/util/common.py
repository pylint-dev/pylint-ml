from astroid import nodes


def get_method_name(node: nodes.Call) -> str:
    """Extracts the method name from a Call node, including handling chained calls."""
    func = node.func
    while isinstance(func, nodes.Attribute):
        func = func.expr
    return (
        node.func.attrname
        if isinstance(node.func, nodes.Attribute)
        else func.name if isinstance(func, nodes.Name) else ""
    )


def get_full_method_name(node: nodes.Call) -> str:
    func = node.func
    method_chain = []

    while isinstance(func, nodes.Attribute):
        method_chain.insert(0, func.attrname)
        func = func.expr
    if isinstance(func, nodes.Name):
        method_chain.insert(0, func.name)

    return ".".join(method_chain)
