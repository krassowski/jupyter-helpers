import html
from types import SimpleNamespace

import pandas as pd
from IPython.core.display import display, HTML


class NeatNamespace(SimpleNamespace):

    __name__ = 'Namespace'

    def __init__(self, *args, **kwargs):
        if not kwargs and args:
            assert args and len(args) == 1
            kwargs = args[0]
            kwargs = {str(k): v for k, v in kwargs.items()}
            if isinstance(kwargs, SimpleNamespace):
                kwargs = kwargs.__dict__
        super().__init__(**kwargs)

    def _body_vertical(self, data):
        body = ''
        for k, v in data:
            body += f'<tr><td><b>{k}</b></td><td>{v}</td></tr>'
        return body

    def _body_horizontal(self, data):
        body = ''
        body += '<tr>'
        for k, v in data:
            body += f'<td><b>{k}</b></td>'
        body += '</tr>'
        body += '<tr>'
        for k, v in data:
            body += f'<td>{v}</td>'
        body += '</tr>'
        return body

    _default_orient = 'vertical'

    def show(self, array_limit=25, list_limit=155, n_rows=None, n_cols=20, head=False, orient=None, render=True):
        if head and not n_rows:
            n_rows = head
        if not n_rows:
            n_rows = 20
        if not orient:
            orient = self._default_orient
        data = []
        for k, v in self.__dict__.items():
            if k == '__name__':
                continue

            if head:
                v = v.head(head)

            if hasattr(v, '_repr_html_'):
                with pd.option_context('display.max_rows', n_rows, 'display.max_columns', n_cols):
                    v = v._repr_html_()
            else:
                ov = v
                shortened = False

                if hasattr(v, 'value'):
                    v = v.value

                try:
                    from numpy import ndarray
                    if isinstance(v, ndarray):
                        v = list(v[:array_limit])
                        shortened = True
                except ImportError:
                    pass

                v = repr(v)

                if len(v) > list_limit:
                    half_limit = list_limit // 2
                    v = v[:half_limit] + ', ..., ' + v[-half_limit:]
                    shortened = True
                try:
                    if shortened:
                        v += f', {len(ov)} in total'
                except Exception:
                    pass
                v = html.escape(v)
            data.append((k, v))

        render_body = self._body_vertical if orient == 'vertical' else self._body_horizontal

        body = render_body(data)

        # header = f'{self.__name__}:' if self.__name__ != 'Namespace' else ''

        repr_str = f"""
        <table class='namespace'>
            {body}
        </table>"""

        if render:
            display(HTML(repr_str))
        else:
            return repr_str

    def _repr_html_(self):
        return self.show(render=False)


class HorizontalNamespace(NeatNamespace):

    _default_orient = 'horizontal'


Namespace = NeatNamespace
