"""System utilities for dynamic resource loading."""

import importlib


def import_namespace(namespace: str) -> type:
    """Import a resource from a namespace string.

    Args:
        namespace (str): The namespace string in the format "module.resource".

    Returns:
        type: The imported resource.

    Raises:
        ValueError: If the namespace string is not in the correct format.
        ImportError: If the module or resource cannot be imported.
        AttributeError: If the resource does not exist in the module.

    Example:
        >>> import_namespace("pactole.data.providers.fdj.FDJResolver")
        <class 'pactole.data.providers.fdj.FDJResolver'>
    """
    if not isinstance(namespace, str) or "." not in namespace.strip("."):
        raise ValueError(f"Invalid namespace format: {namespace}")

    module_name, type_name = namespace.rsplit(".", 1)
    module = importlib.import_module(module_name)

    try:
        return getattr(module, type_name)
    except AttributeError as e:
        raise AttributeError(f"Resource '{type_name}' not found in module '{module_name}'") from e
