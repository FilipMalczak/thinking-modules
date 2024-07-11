# recursive_import

Trivial library that will import the whole module tree.

Main use case for this library is importing everything in given package. Simplest exaple are
decorators that register stuff for CI, a bit like annotation scanning in Java.

> Requires python 3.5+, because of `typing`. Besides that, there are no dependencies.

> System-independent. Tested on CPython 3.9-3.12 (to simplify CI), but its really trivial. 

The whole API is best documented by docstrings:

```python
def package_root(pkg: ModuleType) -> str:
    """
    Find out where is the root directory holding code for specified package or module.
    :param pkg: package to be located.
    :raise ValueError: if the argument is a module and not a package
    :return: absolute path to the directory holding the `__init__` file of the package
    """
    (...)

def current_project_root() -> str:
    """
    Find out where is the root directory holding code for currently running app.
    By "currently running app" we mean the module that is present as `__main__`.
    :return: absolute path to the directory holding the module that is `__main__`
    """
    (...)

def import_package_recursively(root_package: str) -> None:
    """
    Will import the package specified by name and all its subpackages and submodules recursively.
    Order is: each subpackage or submodule of the package, then recurse in that same order.
    :param root_package: name of the package to be scanned. If that's already a subpackage, its parent packages
        will get imported by default (because that's how python works)
    """
    (...)
```

Reading [the test suite](./test/test_recursive_import_from_root.py) is gonna be useful too, in case of uncertainty.