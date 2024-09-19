from importlib.metadata import PackageNotFoundError, version

from pylint.checkers import BaseChecker


class LibraryBaseChecker(BaseChecker):

    def __init__(self, linter):
        super().__init__(linter)
        self.imports = {}

    def visit_import(self, node):
        for name, alias in node.names:
            self.imports[alias or name] = name

    def visit_importfrom(self, node):
        module = node.modname
        print(module)

        for name, alias in node.names:
            print(name)
            print(alias)
            print("-------------")
            full_name = f"{module}.{name}"
            self.imports[alias or name] = full_name

        print(self.imports)

    def is_library_imported_and_version_valid(self, lib_name, required_version):
        """
        Checks if the library is imported and whether the installed version is valid (greater than or equal to the
        required version).

        param lib_name: Name of the library (as a string).
        param required_version: The required minimum version (as a string).
        return: True if the library is imported and the version is valid, otherwise False.
        """
        # Check if the library is imported
        print("xxxxxxxxxxxx")
        print(lib_name)

        if not any(mod.startswith(lib_name) for mod in self.imports.values()):
            return False

        # Check if the library version is valid
        try:
            installed_version = version(lib_name)
        except PackageNotFoundError:
            return False

        # Compare versions (this assumes versioning follows standard conventions like '1.2.3')
        if required_version is not None and installed_version < required_version:
            return False

        return True
