from astroid import nodes


def get_full_method_name(node: nodes.Call) -> str:
    """
    Extracts the full method name from a Call node, including handling chained calls.
    """
    func = node.func
    method_chain = []

    # Traverse the attribute chain to build the full method chain
    while isinstance(func, nodes.Attribute):
        method_chain.insert(0, func.attrname)
        func = func.expr

    # Check if the root of the chain is a Name node (like a module or base name)
    if isinstance(func, nodes.Name):
        method_chain.insert(0, func.name)  # Add the base name

    print(method_chain)
    # Join the method chain to create the full method name
    return ".".join(method_chain)
