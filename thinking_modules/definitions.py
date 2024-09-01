from typing import NamedTuple

from thinking_modules.immutable import Immutable
from thinking_modules.model import ModuleNamePointer, ModuleName

from lazy import lazy

#fixme untested

class type_[T](Immutable):
    clazz: type[T]

    @lazy
    def defining_module(self) -> ModuleName:
        return ModuleName.of(self.clazz)

    def defined_in_module(self, pointer: ModuleNamePointer) -> bool:
        return self.defining_module == ModuleName.resolve(pointer)

    def defined_in_package(self, pointer: ModuleNamePointer) -> bool:
        return self.defining_module.is_descendant(ModuleName.resolve(pointer))


class instance[T](Immutable):
    val: T

    @lazy
    def type_(self) -> type_:
        return type_(type(self.val))
