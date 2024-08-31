import sys
from os.path import basename, dirname, join, exists

from thinking_modules.model import ModuleName

__all__ = [ "main_name", "main_module" ]

main_name = ModuleName.of("__main__")
main_module = main_name.module_descriptor
if main_module.file_path is not None:
    name_parts = [basename(main_module.file_path)[:-len(".py")]]
    parent_dir = dirname(main_module.file_path)
    while exists(join(parent_dir, "__init__.py")):
        name_parts = [basename(parent_dir)] + name_parts
        parent_dir = dirname(parent_dir)
    main_name = ModuleName(name_parts)
    sys.modules[main_name.qualified] = main_module.module_object
    main_module = main_name.module_descriptor