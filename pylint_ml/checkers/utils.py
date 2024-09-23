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


def is_specific_library_object(node: nodes.NodeNG, library_name: str) -> bool:
    """
    Returns True if the given node is an object from the specified library/module.

    Args:
        node: The AST node to check.
        library_name: The name of the library/module to check (e.g., 'pandas', 'numpy').

    Returns:
        bool: True if the node belongs to the specified library, False otherwise.
    """
    return node and node.root().name == library_name  # Checks if the root module matches the library name
