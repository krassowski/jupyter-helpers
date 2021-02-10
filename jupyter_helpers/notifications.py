from pathlib import Path
from time import time
from warnings import warn

from IPython import get_ipython, InteractiveShell
from types import TracebackType

from jupyter_helpers.utilities import play_sound
from jupyter_helpers.desktop_integration import DummyIntegration, GnomeIntegration
from .utilities import scroll_to_current_cell


def _notification_handler(func):
    func.is_notification_handler = True
    return func


def _remove_notification_handlers(ipython):
    for event, callbacks in ipython.events.callbacks.items():
        for callback in callbacks:
            if hasattr(callback, 'is_notification_handler'):
                ipython.events.unregister(event, callback)


def _trim(text, length):
    if len(text) > length:
        text = text[:length] + '...'
    return text


class Notifications:

    integrations = {
        'GNOME': GnomeIntegration,
        None: DummyIntegration
    }

    suggested_sounds = """
        Suggested sounds:
           - beep-07.wav for success, and
           - beep-05.wav for failure (exceptions)
           Due to licensing constraints these cannot be bundled into this package, but can be freely used otherwise.
           Download from: https://www.soundjay.com/beep-sounds-1.html
    """

    def __init__(
        self, success_audio=None, time_threshold=5, failure_audio=None, integration=None,
        hide_after_next_success=True, scroll_to_exceptions='smooth', activate=True,
        smart_scroll=True, max_title_len=50, max_text_len=300
    ):
        f"""Activate notifications after successful completion of computations longer than threshold or after a failure.

        Arguments:
            - success_audio: path to a file with sound to be played once computations finished
            - failure: path to a file with sound to be played on exception
            - threshold: time required to pass between start and the end of computation to generate a beep
            - scroll_to_exceptions: behaviour for scrolling to exceptions (or None to disable)
            - integrate_with: 'GNOME' if you wish to enable GNOME integration
            - smart_scroll: try to avoid scrolling if the cell with exception is already visible on the screen
            - max_title_len: maximal length of the title to show in the notification
            - max_text_len: maximal length of the text to show in the notification

        {self.suggested_sounds}
        """
        if not (success_audio or failure_audio or integration):
            warn('You did not specify neither of paths to the sounds nor requested integration. Are you sure?')
            warn(f'If you do not know what sounds to use, we suggest using:\n{self.suggested_sounds}')

        for path in [success_audio, failure_audio]:
            if path:
                if not Path(path).exists():
                    warn(
                        f'The specified audio path: {path} does not appear to exist. '
                        f'Did you forget to use an absolute path?'
                    )

        if integration is None or isinstance(integration, str):
            integration = self.integrations[integration]

        # parameters
        self.integration = integration()
        self.threshold = time_threshold

        self.success_audio = success_audio
        self.failure_audio = failure_audio

        self.scroll_to_exceptions = scroll_to_exceptions
        self.smart_scroll = smart_scroll
        self.hide_after_next_success = hide_after_next_success

        self.max_title_len = max_title_len
        self.max_text_len = max_text_len

        # state
        self.start_time = None    # time in sec, or None
        self.notify_id = None
        self.exception_notify_id = None
        self.executions_since_error = 0

        if activate:
            self.activate()

    def activate(self):
        ipython = get_ipython()
        _remove_notification_handlers(ipython)
        ipython.events.register('pre_execute', self._pre_execute)
        ipython.events.register('post_execute', self._post_execute)
        ipython.set_custom_exc((Exception,), self._exception_handler)

    @staticmethod
    def deactivate():
        ipython = get_ipython()
        _remove_notification_handlers(ipython)
        ipython.set_custom_exc((Exception, ), None)

    @_notification_handler
    def _pre_execute(self):
        if not self.start_time:
            self.start_time = time()

    @_notification_handler
    def _post_execute(self):
        end_time = time()
        urgency = 'low'
        self.executions_since_error += 1
        if self.executions_since_error > 1:
            self.integration.notify_close(self.exception_notify_id)
        if self.start_time:
            elapsed = end_time - self.start_time
            if elapsed > self.threshold:
                if elapsed > 10 * self.threshold:
                    urgency = 'normal'
                if self.success_audio:
                    play_sound(self.success_audio)
                self.notify_id = self.integration.notify(
                    title='Jupyter is ready',
                    text=f'Done in {elapsed:.2f} s',
                    urgency=urgency,
                    notify_id=self.notify_id
                )
        self.start_time = None

    def _notify_of_exception(self, i_shell, etype, value, tb: TracebackType, tb_offset):
        self.exception_notify_id = self.integration.notify(
            title=_trim(etype.__name__, self.max_title_len),
            text=_trim(str(value), self.max_text_len),
            urgency='critical',
            notify_id=self.exception_notify_id
        )
        self.executions_since_error = 0

    def _exception_handler(self, i_shell: InteractiveShell, etype, value, tb: TracebackType, tb_offset=None):
        i_shell.showtraceback((etype, value, tb), tb_offset=tb_offset)

        self._notify_of_exception(i_shell, etype, value, tb, tb_offset)
        if self.failure_audio:
            play_sound(self.failure_audio)
        if self.scroll_to_exceptions:
            scroll_to_current_cell(self.scroll_to_exceptions, smart=self.smart_scroll)
