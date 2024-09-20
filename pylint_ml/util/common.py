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


def get_full_method_name(lib_alias: str, node: nodes.Call) -> str:
    """
    Extracts the full method name, including chained attributes (e.g., np.random.rand).
    """
    func = node.func
    method_chain = []

    # Traverse the attribute chain
    while isinstance(func, nodes.Attribute):
        method_chain.insert(0, func.attrname)
        func = func.expr

    # Check if the root of the chain is "np" (as NumPy functions are expected to use np. prefix)
    if isinstance(func, nodes.Name) and func.name == lib_alias:
        return ".".join(method_chain)
    return ""
