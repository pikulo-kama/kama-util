import importlib
import inspect
import pkgutil
import sys
from typing import Callable


def get_members(package: str, clazz: type):
    """
    Used to get tuple of class name, class that
    correspond to provided type and located in
    provided package.

    Iterates through all modules within the specified package path, imports
    them dynamically, and yields classes that are subclasses of the
    provided type (excluding the type itself).
    """

    for _, module_name, _ in pkgutil.iter_modules(sys.modules[package].__path__):
        module = importlib.import_module(f"{package}.{module_name}")

        for member_name, member in inspect.getmembers(module, inspect.isclass):

            if issubclass(member, clazz) and member is not clazz:
                yield member_name, member


def get_methods(target, name_filter: Callable[[str], bool]):
    """
    Used to extract methods from a target object based on a name filter.

    Inspects the attributes of the target object and yields the name and
    method reference for all members that are callable, identified as
    methods, and pass the provided filter criteria.
    """

    for name in dir(target):
        if not name_filter(name):
            continue

        member = getattr(target, name)

        if callable(member) and inspect.ismethod(member):
            yield name, member
