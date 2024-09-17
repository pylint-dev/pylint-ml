from pylint.checkers import BaseChecker


class LibraryHandler(BaseChecker):

    def __init__(self, linter):
        super().__init__(linter)
        self.imports = {}

    def visit_import(self, node):
        for name, alias in node.names:
            self.imports[alias or name] = name

    def visit_importfrom(
        self,
        node,
    ):
        # TODO Update method to handle either:
        #   1. Check of specific method-name imported?
        #   2. Store all method names importfrom libname?

        module = node.modname
        for name, alias in node.names:
            full_name = f"{module}.{name}"
            self.imports[alias or name] = full_name

    def is_library_imported(self, library_name):
        return any(mod.startswith(library_name) for mod in self.imports.values())

    # def is_library_version_valid(self, lib_version):
    #     # TODO update solution
    #     if lib_version is None:
    #         pass
    #     return
