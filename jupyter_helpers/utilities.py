from time import sleep
from threading import Thread

from IPython.display import display, Audio

OUTPUT_AREA_CLASS = 'jp-OutputArea-child'
OUT_CLASS = 'jp-transient-html'


def try_to_hide_parent(css_class, level):
    """deprecated"""
    return (
        f'var parent = this{".parentNode" * level};'
        f'if(parent.className == \'{css_class}\') parent.style.display = \'none\';'
    )


def hide_closest(css_class):
    return (
        f"var widget_our = this.closest('.{OUT_CLASS}');"
        f"var that = widget_our ? widget_our : this;"
        f"that.closest('.{css_class}').style.display = 'none';"
    )


def delete_closest(css_class):
    return (
        f"var widget_our = this.closest('.{OUT_CLASS}');"
        f"var that = widget_our ? widget_our : this;"
        f"var el = that.closest('.{css_class}'); el.parentNode.removeChild(el);"
    )


def delete_element(levels_up=1):
    return (
        'this'
        + '.parentNode' * levels_up
        + '.removeChild('
          + 'this'
          + '.parentNode' * (levels_up - 1)
        + ')'
    )


class InvisibleAudio(Audio):

    def _repr_html_(self):
        audio = super()._repr_html_()
        audio = audio.replace(
            '<audio',
            (
                '<audio onended="'
                + hide_closest(css_class=OUTPUT_AREA_CLASS)
                + '" onloadstart="' + hide_closest(css_class=OUTPUT_AREA_CLASS) + '"'
            )
        )
        return f'<div style="display:none">{audio}</div>'


def javascript_in_jupyter(code):
    return f'<img onerror="{code}" src="x" style="display:none"></div>'


def delayed_close(out, element, delay):
    sleep(delay)
    element.close()
    out.clear_output()
    out.close()


def transient_html(code: str, lifetime: float = 3):
    """Attempts to display and then hide given HTML code.

    If the hiding is not possible (no ipywidgets) fall-backs to persistent display.

    Arguments:
        code: HTML code as a string
        lifetime: time
    """
    try:
        from ipywidgets import HTML
        from ipywidgets.widgets import Output
        element = HTML(code)
        out = Output()
        out.add_class(OUT_CLASS)

        thread = Thread(target=delayed_close, args=(out, element, lifetime))

        with out:
            display(element)

        display(out)

        thread.start()

    except ImportError:
        from IPython.display import HTML
        element = HTML(code)
        display(element)


def scroll_to_current_cell(
    scroll_behaviour='smooth',
    preserve=False,
    smart=True,
    scroll_to='center',
    cell_class='jp-Cell'
):
    behaviour = f"behavior: '{scroll_behaviour}', block: '{scroll_to}'"
    code = (
        # scroll to the output
        '\n'.join([
            f"let cell = this.closest('.{cell_class}');",
            'let rect = cell.getBoundingClientRect();',
            (
                (
                    'let is_visible = rect.top >= 0 &&'
                    ' rect.bottom <= (window.innerHeight || document.documentElement.clientHeight);'
                )
                if smart else
                'let is_visible = false;'
            ),
            'if (!is_visible) {',
            '    cell.scrollIntoView({' + behaviour + '});',
            '}'
        ])
        # hide the output generated as an anchor
        + hide_closest(css_class=OUTPUT_AREA_CLASS)
    )
    code = javascript_in_jupyter(code)

    if not preserve:
        transient_html(code)

    if preserve:
        from IPython.display import HTML
        element = HTML(code)
        display(element)


def play_sound(filename):
    audio = InvisibleAudio(filename=filename, autoplay=True)
    transient_html(audio._repr_html_())
