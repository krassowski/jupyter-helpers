from rpy2.robjects import r
from IPython import get_ipython


def rpy2_completer(ipython, event):
    query = event.line.strip().split()[-1]
    suggestions = []
    all_r_symbols = r('sapply(search(), ls)')
    for environment, symbols in all_r_symbols.items():
        for _, symbol in symbols.items():
            if symbol.startswith(query):
                suggestions.append(symbol)
    return suggestions


ipython = get_ipython()
ipython.set_hook('complete_command', rpy2_completer, re_key='.*')
