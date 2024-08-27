# thinking-modules

[![CI](https://github.com/FilipMalczak/thinking-modules/actions/workflows/ci.yml/badge.svg)](https://github.com/FilipMalczak/thinking-modules/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/thinking-modules.svg)](https://badge.fury.io/py/thinking-modules)

> Part of [thinking](https://github.com/search?q=owner%3AFilipMalczak+thinking&type=repositories) family.

Module-related python utilities - recursive package import, modeling of names and modules, etc

Main use case for this library is importing everything in given package. Simplest example are
decorators that register stuff for CI, a bit like annotation scanning in Java.

Besides that provides models and related utilities for modules and their names.

> Requires python 3.12. Is properly typed.  

## API

The whole API is best documented by docstrings below. 
Reading [the test suite](./test/test_recursive_import_from_root.py) is gonna be useful too, in case of uncertainty.

### [thinking_modules.model](./thinking_modules/model.py)

```python
class ModuleKind(Enum):
    MODULE = auto()
    """Represents non-package module"""
    
    PACKAGE = auto()
    """Represent __init__.py file of a package"""
    
    PACKAGE_MAIN = auto()
    """Represents __main__.py file of a package"""
    
    SHELL = auto()
    """Represents interactive shell session or running with 'python -c ...'"""


type ModulePointer = str | ModuleName | ModuleType

type ModuleNamePointer = ModulePointer | list[str] | object


class Module(NamedTuple):
    module_: ModuleType
    file_path: Optional[str]
    name: 'ModuleName'
    kind: ModuleKind

    @property
    def is_package(self) -> bool: (...)

    @property
    def is_shell(self) -> bool: (...)

    @property
    def is_module(self) -> bool: (...)

    @classmethod
    def find(cls, pointer: ModulePointer, *, evaluate_if_missing: bool = True) -> ModuleType: 
        """
        Turn the pointer to the module (of typing.ModuleType type).

        Pointer may be a ModuleName or str (being an unparsed version of module name) or module itself (in which case
        this method is passthrough).

        If module hasn't been imported yet (is not present in sys.modules), behaviour depends on evaluate_if_missing.
        If that argument is True, the module will be imported; if False, KeyError will be raised.

        :raise KeyError: if module hasn't been ever imported and evaulate_if_missing is False.
        :return: raw python module
        """

    @classmethod
    def resolve(cls, pointer: ModulePointer, *, evaluate_if_missing: bool = True) -> Self:
        """
        Find the module (with Module.find(...); both arguments are forwarded there) and describe it to obtain an instance
        of Module.

        :raise KeyError: in the same case as Module.find(...)
        :return: descriptor of the module
        """
        
class ModuleName(NamedTuple):
    parts: list[str]

    @property
    def qualified(self) -> str:
        """
        :return: Full, dot-separated name represented by this instance.
        """

    @property
    def simple(self) -> str:
        """
        :return: Part after the last dot in qualified name. Name (w/o extension) of the file holding the module or
                directory holding the package.
        """

    @property
    def root_package(self) -> Optional[str]:
        """
        :return: Part before the first dot in qualified name, or None in case of a module lying outside of package.
        """

    @property
    def parent(self) -> Optional[Self]:
        """
        :return: ModuleName of the package in which the module/package named with this instance resides in, or None in
                case of root packages and non-packaged modules.
        """

    @property
    def has_been_evaluated(self) -> bool:
        """
        :return: Has the import of module with that name happened? Mind you that pkg.__main__ is represented as name pkg.
        """

    @classmethod
    def resolve(cls, something: ModuleNamePointer) -> Self:
        """
        - If argument is already a ModuleName, then this method is pass-through.
        - If argument is str assumes that it's a raw module/package name.
        - If argument is list of str, assumes that it's previous case split over dot.
        - If argument is a module (of type typing.ModuleType), parses its name. In case of packages, both __init__.py
          and __main__.py will evaluate to the package name itself.
        - In any other case will retrieve module in which the object has been defined and parse it.
        """


```

### [thinking_modules.importing](./thinking_modules/importing.py)

```python

def package_root(pkg: ModulePointer) -> str:
    """
    Find out where is the root directory holding code for specified package.
    :param pkg: package to be located.
    :raise ValueError: if the argument is a module and not a package
    :return: absolute path to the directory holding the `__init__` file of the package
    """

def current_project_root() -> str:
    """
    Find out where is the root directory holding code for currently running app.
    By "currently running app" we mean the module that is present as `__main__`.
    :return: absolute path to the directory holding the module that is `__main__`
    """


def import_package_recursively(root_package: str) -> list[ModuleName]:
    """
    Will import the package specified by name and all its subpackages and submodules recursively.

    Order is: the package itself, each direct submodule in default sorted() order, then recurse into subpackages in
    default sorted() order.

    :param root_package: name of the package to be scanned. If that's already a subpackage, its parent packages
        will get imported by default (because that's how python works)
    :return: list of imported ModuleNames, in order of importing
    """
```