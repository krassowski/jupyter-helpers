import ast

import nbimporter

from IPython import get_ipython
from IPython.core import magic


@magic.register_cell_magic
def skip_on_import(args, cell):
    get_ipython().ex(cell)


class SkippingTransformer(ast.NodeTransformer):

    def visit(self, node):
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute)
            and node.value.func.attr == 'run_cell_magic'
            and node.value.args[0].s == 'skip_on_import'
        ):
            return
        return node


nbimporter.CellDeleter = SkippingTransformer
notebooks_importer = nbimporter


__all__ = ['skip_on_import', 'notebooks_importer']
