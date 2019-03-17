from inspect import getsource

from IPython.core.display import HTML, display
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

_formatter = HtmlFormatter()


def get_source(obj, preprocess=None):
    # comments = f'# decorated by: {obj.decorated_by}\n' if hasattr(obj, 'decorated_by') else ''
    if hasattr(obj, 'original_function'):
        obj = obj.original_function
    if hasattr(obj, '__source__'):
        source = obj.__source__
    else:
        source = getsource(obj)
    if preprocess:
        source = preprocess(source)
    return HTML(highlight(source, PythonLexer(), _formatter))


def show_source(obj):
    display(get_source(obj))


def embed_source_styling(custom_styles='.highlight{margin-left:10px!important; font-size:11px}'):
    default_highlight_style = _formatter.get_style_defs('.highlight')
    html = HTML(f'<style>{default_highlight_style}{custom_styles}</style>')
    display(html)
