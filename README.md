# thinking-modules

[![CI](https://github.com/FilipMalczak/thinking-modules/actions/workflows/ci.yml/badge.svg)](https://github.com/FilipMalczak/thinking-modules/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/thinking-modules.svg)](https://badge.fury.io/py/thinking-modules)
[![cov](https://FilipMalczak.github.io/thinking-modules/badges/coverage.svg)](https://github.com/FilipMalczak/thinking-modules/actions)


> Part of [thinking](https://github.com/search?q=owner%3AFilipMalczak+thinking&type=repositories) family.

Module-related python utilities - recursive package scan and import, modeling of names and modules, etc

Main use case for this library is importing everything in given package. Simplest example are
decorators that register stuff for CI, a bit like annotation scanning in Java, which need to be triggered/executed
before the main portion of your program.

Besides that provides models and related utilities for modules and their names.

> Requires python 3.12. Is properly typed.  

## API

The code is pretty self-documenting (meaning "browse the code, don't expect Sphinx"). It is organized into following modules:
- [`thinking_modules.model`](./thinking_modules/model.py)
  - `ModuleName`
    - represent module or package name
    - doesn't import the module, is just a pointer
    - allows for easy modeling of subpackages, submodules, parent packages, etc
    - can refer to non-existent modules
  - `ModuleNamePointer`
    - union type representing everything that can be parsed to `ModuleName` - a `str`, module itself, etc
  - `Module`
    - is a descriptor over a python module or package
    - may refer to non-existing piece of code, but will raise exception when using most methods
    - allows you to recognize whether something is a module, package, `pkg.__main__` file or shell session
    - exposes some other useful info, like whether a module has been already imported, where is it located in filesystem
      (if anywhere), what is its root package and allows you to import it with `importlib`
  - most properties of `Module` and `ModuleName` are lazy and cached, so, for example, if you create a `Module` pointing
    to a non-existent piece of code, it won't raise exception until you actually access `m.module_object`; similarly,
    once you access `m.kind`, it will be cached and will be quickly accessible next time you access it
  - kudos to [`lazy`](https://pypi.org/project/lazy/) for that
- [`thinking_modules.scan`](./thinking_modules/scan.py)
  - holds a single function: `scan(pkg: ModuleNamePointer)`
  - that function takes a package name (fails if given a non-package module name)
  - it analyses filesystem, trying to find all the module names within the tree stemming from that package
- [`thinking_modules.main_modules`](./thinking_modules/main_module.py)
  - when we're running anything, its name becomes `__main__`
  - that module still should be accessible by name based on its filepath
  - for example, if you do `python -m pkg.subpkg.mod`, you'll execute file `.../pkg/subpkg/mod.py` which otherwise
    would be available as `pkg.subpkg.mod`, but in such runtime will have `__name__` `__main__`
  - this module will analyse (on import) file structure, and expose `main_name` (of type `ModuleName`) and `main_module`
    (of type `Module`) that describe `pkg.subpkg.mod` (as opposed to `__main__`)
  - it will also (on import) alias `pkg.subpkg.mod` in `sys.modules` to `__main__`, so you can safely do circular imports
- [`thinking_modules.definitions`](./thinking_modules/definitions.py)
  - micro-DSL for queries like:
    - `instance(SomeClass()).type_.defining_module`
    - `type_(SomeClass).defining_module` (equivalent to the one above)
    - `instance(...).type_.defined_in_module("pkg.mod")`
    - `instance(...).type_.defined_in_package("pkg")` (meaning "in package `pkg` or any of its subpackages or submodules)
  - nothing complicated, but makes for readable metaprogramming code
- [`thinking_modules.immutable`](./thinking_modules/immutable.py)
  - helper module for something that emulates `NamedTuple`, while allowing for `lazy` properties
  - not really related to domain of this project, strictly technical, but pretty useful util
  - is needed, as `lazy` works around the `__dict__`, which is lacking in `NamedTuple`s

Reading [the test suite](./test) is gonna be useful too, in case of uncertainty.