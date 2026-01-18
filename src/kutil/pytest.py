

def safe_patch(patch_method, path, *args, **kw):
    """
    Attempts to patch a target path and returns a MagicMock if the path is invalid.

    This function wraps the standard patch method to catch AttributeErrors,
    ensuring that tests do not crash if a targeted attribute or module
    is missing from the current environment.
    """

    from unittest.mock import MagicMock

    try:
        return patch_method(path, *args, **kw)
    except AttributeError:
        return MagicMock()


def safe_patch_fixture(mocker):
    """
    Provides a functional wrapper for performing safe patches using the mocker fixture.

    Returns a lambda that passes the mocker's patch method into the
    safe_patch logic.
    """
    return lambda path, *args, **kw: safe_patch(mocker.patch, path, *args, **kw)


def safe_module_patch_fixture(module_patch):
    """
    Provides a functional wrapper for performing safe patches on module-level targets.

    Similar to safe_patch_fixture, but utilizes the get_module_patch
    factory to resolve paths relative to the source module.
    """
    return lambda path, *args, **kw: safe_patch(module_patch, path, *args, **kw)


def module_path_fixture(request, pytestconfig):
    """
    Resolves the source module path corresponding to the current test module.

    Parses the test module's name to determine the equivalent source code
    location, handling standard file naming conventions and the special
    case of package initialization files.
    """

    plugin = pytestconfig.pluginmanager.get_plugin("_cov")

    if not plugin or not plugin.cov_controller or not plugin.cov_controller.cov:
        raise RuntimeError("Coverage controller is not configured.")

    base_package = plugin.cov_controller.cov.config.source[0]
    separator = "."

    path_list = str(request.module.__name__).split(separator)
    test_name = path_list.pop()
    source_file_name = test_name.replace("test_", "")

    # Replace base package.
    path_list.insert(0, base_package)

    # File called 'test_init' should test __init__.py file of module,
    # so we shouldn't add it to path.
    if source_file_name != "init":
        path_list.append(source_file_name)

    return separator.join(path_list)


def module_patch_fixture(mocker, module_path):
    """
    Used to resolve module level mocks.

    It would be transformed by replacing first part of path
    with root package (savegem) as well as removing test_
    prefix from file name.

    Example of transformation:
    - tests.common.core.test_app_state
    - savegem.common.core.app_state

    Returns a factory function that generates patchers scoped to the
    current test's corresponding source module.
    """
    return lambda path, *args, **kw: mocker.patch(f"{module_path}.{path}", *args, **kw)
