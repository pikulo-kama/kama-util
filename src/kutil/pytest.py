

def safe_patch(patch_method, path, *args, **kw):
    from unittest.mock import MagicMock

    try:
        return patch_method(path, *args, **kw)
    except AttributeError:
        return MagicMock()

def safe_patch_fixture(mocker):
    return lambda path, *args, **kw: safe_patch(mocker.patch, path, *args, **kw)

def safe_module_patch_fixture(get_module_patch):
    return lambda path, *args, **kw: safe_patch(get_module_patch, path, *args, **kw)

def module_path_fixture(request):
    def get_module_path(root_package_path: str):
        separator = "."

        path_list = str(request.module.__name__).split(separator)
        test_name = path_list.pop()
        source_file_name = test_name.replace("test_", "")

        # Replace base package.
        if len(path_list) > 0:
            path_list[0] = root_package_path
        else:
            path_list.append(root_package_path)

        # File called 'test_init' should test __init__.py file of module,
        # so we shouldn't add it to path.
        if source_file_name != "init":
            path_list.append(source_file_name)

        return separator.join(path_list)

    return get_module_path

def get_module_patch_fixture(mocker, module_path):
    """
    Used to resolve module level mocks.

    It would be transformed by replacing first part of path
    with root package (savegem) as well as removing test_
    prefix from file name.

    Example of transformation:
    - tests.common.core.test_app_state
    - savegem.common.core.app_state
    """

    def _get_patch(root_package_path: str):
        def _patch(path, *args, **kw):
            mock_path = f"{module_path(root_package_path)}.{path}"
            return mocker.patch(mock_path, *args, **kw)

        return _patch

    return _get_patch