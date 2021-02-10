from abc import ABC, abstractmethod
from pathlib import Path
from subprocess import check_output, call

ROOT = Path(__file__).parent


class DesktopIntegration(ABC):

    @abstractmethod
    def notify(self, title, text, notify_id=None, show_again=True, urgency='normal', expire_time=60):
        pass

    @abstractmethod
    def notify_close(self, notify_id):
        pass


class GnomeIntegration(DesktopIntegration):

    def __init__(self):
        drop_in_replacement = Path(ROOT / 'thirdparty/notify-send/notify-send.sh')
        self.app = (
            drop_in_replacement.as_posix()
            if drop_in_replacement.exists() else
            'notify-send'
        )
        self.using_drop_in_replacement = drop_in_replacement.exists()

    def notify(self, title, text, notify_id=None, show_again=True, urgency='normal', expire_time=60):

        arguments = [title, text, f'--urgency={urgency}']

        if self.using_drop_in_replacement:
            arguments.append('--print-id')
            if notify_id and not show_again:
                arguments.append(f'--replace={notify_id}')
        else:
            arguments.append(f'--hint=int:transient:{expire_time}')
            arguments.append(f'--expire-time={expire_time}')

        if show_again and notify_id:
            self.notify_close(notify_id)
        output = check_output([self.app] + arguments)
        if output:
            notify_id = output.strip().decode('utf-8')
            return notify_id

    def notify_close(self, notify_id):
        # the basic notify-send cannot close notifications
        if self.using_drop_in_replacement:
            call([self.app, f'--close={notify_id}'])


class DummyIntegration(DesktopIntegration):

    def notify(self, title, text, notify_id=None, show_again=True, urgency='normal'):
        pass

    def notify_close(self, notify_id):
        pass
