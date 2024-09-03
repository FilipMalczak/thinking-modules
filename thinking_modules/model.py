import sys
from enum import Enum, auto
from importlib import import_module
from os.path import basename
from types import ModuleType
from typing import Optional, Self

from lazy import lazy

from thinking_modules.immutable import Immutable

#fixme some methods are marked as "roughly tested"; they are tested, but not very deeply
# cost of testing these would be way too high for now

class ModuleKind(Enum):
    MODULE = auto()
    """Represents non-package module"""

    PACKAGE = auto()
    """Represent __init__.py file of a package"""

    PACKAGE_MAIN = auto()
    """Represents __main__.py file of a package"""

    SHELL = auto()
    """Represents interactive shell session or running with 'python -c ...'"""

#todo Module should also be a module name pointer
type ModuleNamePointer = str | list[str] | ModuleName | ModuleType | object


class Module(Immutable):
    name: 'ModuleName'

    @lazy
    def module_object(self) -> ModuleType:
        """
        :raise ModuleNotFound:
        """
        return import_module(self.name.qualified)

    @property
    def is_imported(self) -> bool:
        return self.name.qualified in sys.modules

    @lazy
    def file_path(self) -> Optional[str]:
        try:
            return self.module_object.__file__
        except AttributeError:
            return None

    @lazy
    def kind(self) -> ModuleKind:
        if self.file_path is None:
            return ModuleKind.SHELL
        filename = basename(self.file_path)
        if filename == "__init__.py":
            return ModuleKind.PACKAGE
        elif filename == "__main__.py" and self.name.parent is not None:
            return ModuleKind.PACKAGE_MAIN
        else:
            return ModuleKind.MODULE

    @lazy
    def is_package(self) -> bool:
        return self.kind == ModuleKind.PACKAGE

    @lazy
    def is_shell(self) -> bool:
        return self.kind == ModuleKind.SHELL

    @lazy
    def root_package_name(self) -> Optional['ModuleName']:
        if len(self.name) > 1:
            return ModuleName([self.name.parts[0]])
        if self.is_package:
            return self.name
        return None

    #fixme roughly tested
    @lazy
    def canonical_name(self) -> 'ModuleName':
        return ModuleName.of(self.module_object)

    #fixme roughly tested
    @lazy
    def is_main(self) -> bool:
        return self.canonical_name.qualified == "__main__"


class ModuleName(Immutable):
    parts: list[str]

    @lazy
    def qualified(self) -> str:
        """
        :return: Full, dot-separated name represented by this instance.
        """
        return ".".join(self.parts)

    @lazy
    def simple(self) -> str:
        """
        :return: Part after the last dot in qualified name. Name (w/o extension) of the file holding the module or
                directory holding the package.
        """
        return self.parts[-1]

    @lazy
    def parent(self) -> Optional[Self]:
        """
        :return: ModuleName of the package in which the module/package named with this instance resides in, or None in
                case of root packages and non-packaged modules.
        """
        if len(self.parts) == 1:
            return None
        return ModuleName(self.parts[:-1])

    #fixme tested indirectly, via definitions
    def is_ancestor(self, other: Self) -> bool:
        if len(other) < len(self):
            return False
        return self.parts == other.parts[:len(self.parts)]

    #fixme tested indirectly, via definitions
    def is_descendant(self, other: Self) -> bool:
        return other.is_ancestor(self)

    def submodule(self, name: str) -> Self:
        """
        Assume that this name refers to a package and return a ModuleName pointing to module or package with given name
         residing in that package.
        :param name: name of submodule or subpackage
        :return: child name
        """
        assert name #msg
        return ModuleName(self.parts + [name])

    @lazy
    def module_descriptor(self) -> Module:
        return Module(self)

    def import_(self) -> ModuleType:
        return self.module_descriptor.module_object

    @classmethod
    def resolve(cls, something: ModuleNamePointer) -> Self:
        """
        - If argument is already a ModuleName, then this method is pass-through.
        - If argument is str assumes that it's a raw module/package name.
        - If argument is list of str, assumes that it's previous case split over dot.
        - If argument is a module (of type typing.ModuleType), parses its name
        - In any other case will retrieve module in which the object type has been defined and parse it.
        """
        if isinstance(something, ModuleName):
            return something
        name = None
        parts = None
        if isinstance(something, str):
            parts = something.split(".")
        elif isinstance(something, ModuleType):
            name = something.__name__
        elif isinstance(something, list):
            assert all(isinstance(x, str) for x in something)  # todo msg
            parts = something
        else:
            name = something.__module__
        if parts is None:
            parts = name.split(".")
        #fixme check if this is left in docs, remove it
        #if declared in __main__ module - keep the name
        #if declared in pkg.__main__ - skip __main__, keep the pkg
        #fixme this will screw up import from pkg.__main__ - get rid of this beature? or actually reenable it?
        # if parts[-1] == "__main__" and len(parts) > 1:
        #     parts = parts[:-1]
        return ModuleName(parts)

    of = resolve

    #fixme untested
    @lazy
    def is_canonical(self) -> bool:
        return self.canonical == self

    #fixme untested
    @lazy
    def canonical(self) -> Self:
        return self.module_descriptor.canonical_name

    def __len__(self):
        return len(self.parts)

    def __str__(self):
        return f"{type(self).__name__}.of('{self.qualified}')"