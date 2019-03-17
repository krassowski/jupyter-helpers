import pandas as pd
from IPython.core.display import display


def bordered_table(hide_headers=[], color='#ddd'):
    return [
        {'selector': 'th', 'props': [('text-align', 'center'), ('border', f'1px solid {color}')]},
        {'selector': 'td', 'props': [('border', f'1px solid {color}')]},
        *[
            {'selector': f'thead tr:nth-child({row})', 'props': [('display', 'none')]}
            for row in hide_headers
        ]
    ]


def display_table(table, n_rows=50, n_cols=None, long_names=-1):
    if not n_cols:
        n_cols = n_rows
    with pd.option_context('display.max_rows', n_rows, 'display.max_columns', n_cols, 'display.max_colwidth', long_names):
        display(table)
