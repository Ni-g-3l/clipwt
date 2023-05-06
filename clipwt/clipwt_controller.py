from clipwt.clipwt_constants import ClipAppStatus
from clipwt.clipwt_model import ClipWtModel


class ClipWtController:

    def __init__(self, model: ClipWtModel) -> None:
        self._model = model

    def set_content(self, clipboard_content):
        stored_content = self._model.content

        if stored_content:
            new_storage_value = f"{stored_content}\n{clipboard_content}"
        else:
            new_storage_value = f"{clipboard_content}"

        if clipboard_content != self._model.old_content:
            self._model.content = new_storage_value
            self._model.old_content = clipboard_content

    def stop_watching(self):
        self._model.status = ClipAppStatus.STOP

    def start_watching(self):
        self._model.status = ClipAppStatus.START

    def clear_storage(self):
        self._model.content = None
        self._model.old_content = None
