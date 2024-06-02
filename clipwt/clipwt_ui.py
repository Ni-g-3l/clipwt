import time
from threading import Thread, Event
import dearpygui.dearpygui as dpg

from clipwt.clipwt_constants import ClipAppStatus

class ClipWtApp:

    def __init__(self, controller) -> None:
        self._controller = controller
        self._model = controller._model
        self.thread = None
        self.event = Event()
        self._init_ui()

    def _init_ui(self):
        dpg.create_context()

        with dpg.window(tag="window"):
            with dpg.group(horizontal=True):
                dpg.add_button(label="Play", callback=self.toggle_state, tag="state_button", width=100)
                dpg.add_button(label="Copy", callback=self.copy_storage, tag="copy_button", width
                               =100)
                dpg.add_button(label="Clear", callback=self.clear_storage, tag="clear_button", width=100)
            dpg.add_separator()
            dpg.add_listbox([], num_items=22, tag="contents", width=320)

        dpg.create_viewport(title="📋 - ClipWt", width=340, height=427)
        dpg.setup_dearpygui()

    def get_clipboard_content(self):
        while self._model.status == ClipAppStatus.START:
            clipboard_content = dpg.get_clipboard_text()
            self._controller.set_content(clipboard_content)

            if self._model.content:
                dpg.configure_item("contents", items=self._model.content.split("\n"))
            time.sleep(2)

    def stop_watching(self):
        self.event.clear()
        self._model.status = ClipAppStatus.STOP
        self._controller.stop_watching()
        dpg.configure_item("state_button", label="Play", callback=self.toggle_state)

    def toggle_state(self):
        self._model.status = ClipAppStatus.START
        self._controller.start_watching()
        dpg.configure_item("state_button", label="Stop", callback=self.stop_watching)
        self.thread = Thread(target=self.get_clipboard_content)
        self.thread.start()

    def clear_storage(self):
        self._controller.clear_storage()
        dpg.configure_item("contents", items=[])

    def copy_storage(self):
        self.stop_watching()
        dpg.set_clipboard_text(self._model.content)

    def show(self):
        dpg.show_viewport()
        dpg.set_primary_window("window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
