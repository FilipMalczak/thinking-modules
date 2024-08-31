from logging import getLogger
from os import listdir
from os.path import basename, join, exists, dirname, isdir
from typing import Iterable

from thinking_modules.model import ModuleName, ModuleNamePointer

log = getLogger(__name__)

def scan(pkg_name: ModuleNamePointer, *, include_mains: bool=False) -> Iterable[ModuleName]:
    pkg_name = ModuleName.resolve(pkg_name)
    assert pkg_name.python_module.is_package
    def scan_pkg(name: ModuleName, pkg_dir: str):
        log.debug(f"Found package {name.qualified}")
        yield name
        log.debug(f"Scanning {name.qualified} in {pkg_dir}")
        subpkgs: list[tuple[ModuleName, pkg_dir]] = []
        for entry in sorted(listdir(pkg_dir)):
            path = join(pkg_dir, entry)
            if isdir(path):
                if exists(join(path, "__init__.py")):
                    log.debug(f"{path} holds a package, enqueuing for scan")
                    subpkgs.append((name.submodule(entry), path))
                else:
                    log.debug(f"{path} is not a package, not going deeper")
            else:
                filename = basename(path)
                if path.endswith(".py"):
                    if filename == "__init__.py":
                        log.debug("Skipping __init__.py of current package")
                    elif filename == "__main__.py" and not include_mains:
                        log.debug("Skipping __main__.py of current package")
                    else:
                        log.debug(f"Found a python module under {path}")
                        yield name.submodule(filename[:-len('.py')])
                else:
                    log.debug(f"Ignoring non-python-source file {path}")
        for sub in subpkgs:
            yield from scan_pkg(*sub)
    yield from scan_pkg(pkg_name, dirname(pkg_name.python_module.file_path))