from time import sleep

from IPython.display import display, Audio


def try_to_hide_parent(css_class, level):
    return (
        f'var parent = this{".parentNode" * level};'
        f'if(parent.className == \'{css_class}\') parent.style.display = \'none\';'
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
                + try_to_hide_parent(css_class='jp-RenderedHTML', level=4)
                + delete_element()
                + '"'
            )
        )
        return f'<div style="display:none">{audio}</div>'


def javascript_in_jupyter(code):
    return f'<img onerror="{code}" src="x" style="display:none"></div>'


def transient_html(code: str, lifetime: float = 1):
    """Attempts to display and then hide given HTML code.

    If the hiding is not possible (no ipywidgets) fall-backs to persistent display.

    Arguments:
        code: HTML code as a string
        lifetime: number of seconds to wait before closing
    """
    try:
        from ipywidgets import HTML
        element = HTML(code)

        def delayed_close():
            sleep(lifetime)
            element.close()
        display(element)
        element.on_displayed(delayed_close())

    except ImportError:
        element = HTML(code)
        display(element)


def scroll_to_current_cell(scroll_behaviour='smooth', preserve=False):
    code = (
        # scroll to the output
        f'this.parentElement.parentElement.parentElement.parentElement.parentElement.scrollIntoView({{behavior: \'{scroll_behaviour}\'}});'
        # hide the output generated as an anchor
        + try_to_hide_parent(css_class='jp-RenderedHTML', level=3)
        # delete the javascript
        + delete_element()
    )
    code = javascript_in_jupyter(code)

    fallback = False
    if not preserve:
        transient_html(code)

    if preserve or fallback:
        from IPython.display import HTML
        element = HTML(code)
        display(element)


def play_sound(filename):
    audio = InvisibleAudio(filename=filename, autoplay=True)
    transient_html(audio._repr_html_())
