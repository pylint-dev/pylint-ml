from astroid import nodes
from pylint.checkers.utils import safe_infer


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


def infer_module_from_node_chain(start_node: nodes.NodeNG, module_name: str) -> bool:
    """
    Traverses the chain of attributes and checks if the root module of the node chain
    matches the specified module name (e.g., 'numpy' or 'pandas').

    Args:
        start_node (nodes.NodeNG): The starting node (either Attribute or Call).
        module_name (str): The module name to check against (e.g., 'numpy', 'pandas').

    Returns:
        bool: True if the root module matches the specified module_name, False otherwise.
    """
    current_node = start_node

    # Traverse backward through the chain, handling Attribute and Name node types
    while isinstance(current_node, (nodes.Attribute, nodes.Name)):
        if isinstance(current_node, nodes.Attribute):
            # Infer the current expression (e.g., np.some)
            inferred_object = safe_infer(current_node.expr)
            if inferred_object is None:
                return False
            current_node = current_node.expr  # Step backwards
        elif isinstance(current_node, nodes.Name):
            # Base case: a Name node is likely a module or variable (e.g., 'np')
            inferred_root = safe_infer(current_node)
            if inferred_root:
                # Check if the inferred object's name matches the module_name
                if inferred_root.qname() == module_name:
                    return True
                else:
                    return False
            else:
                return False  # If inference of the Name node fails

    return False  # Return False if we couldn't infer a valid module


def infer_specific_module_from_call(node: nodes.Call, module_name: str) -> bool:
    """
    Infers if the function call belongs to the specified module (e.g., 'numpy', 'pandas').

    Args:
        node (nodes.Call): The Call node representing the method call.
        module_name (str): The module name to check against (e.g., 'numpy', 'pandas').

    Returns:
        bool: True if the root module matches the specified module_name, False otherwise.
    """
    return infer_module_from_node_chain(node.func, module_name)


def infer_specific_module_from_attribute(node: nodes.Attribute, module_name: str) -> bool:
    """
    Infers if the attribute access belongs to the specified module (e.g., 'numpy', 'pandas').

    Args:
        node (nodes.Attribute): The Attribute node representing the method or attribute access.
        module_name (str): The module name to check against (e.g., 'numpy', 'pandas').

    Returns:
        bool: True if the root module matches the specified module_name, False otherwise.
    """
    return infer_module_from_node_chain(node, module_name)
