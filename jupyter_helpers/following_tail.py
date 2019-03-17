from abc import ABC, abstractmethod
from warnings import warn

from IPython.core.display import clear_output, display, HTML


def display_one_at_a_time(text):
    clear_output(wait=True)
    display(text)


class AbstractFollowingTail(ABC):

    def __init__(self, n=5):
        self.n = n

    def activate(self):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class SimpleFollowingTail(AbstractFollowingTail):

    def __init__(self, n=1):
        if n != 1:
            try:
                from ipywidgets import Output
                warn('To use n > 1, please use PyWidgetsInteractiveTail')
            except ImportError:
                warn('To enable use of n > 1, please install ipywidgets package')
            warn('Using n = 1')
        super().__init__(n)

    def __call__(self, text):
        return display_one_at_a_time(text)


try:
    from ipywidgets import Output

    def pack_to_div(obj):
        data = obj._repr_html_() if hasattr(obj, '_repr_html_') else str(obj)
        return f'<div>{data}</div>'

    class PyWidgetsFollowingTail(AbstractFollowingTail):

        def __init__(self, n=5):
            super().__init__(n)
            self.output = Output()
            self.buffer = []

        def activate(self):
            display(self.output)

        def __call__(self, text):
            if len(self.buffer) == self.n:
                self.buffer = self.buffer[1:]
            self.buffer.append(text)
            with self.output:
                display(HTML(
                    ''.join(map(pack_to_div, self.buffer))
                ))
                clear_output(wait=True)

    FollowingTail = PyWidgetsFollowingTail

except ImportError:

    FollowingTail = SimpleFollowingTail
