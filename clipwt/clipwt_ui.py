import os
import tkinter as tk
from tkinter import *
import customtkinter
from PIL import Image

from clipwt.clipwt_constants import CLEAR_ICON_PATH, CLIP_ICON_PATH, ICON_SIZE, PLAY_ICON_PATH, STOP_ICON_PATH, ClipAppStatus

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ressources")
PLAY_ICON = customtkinter.CTkImage(Image.open(PLAY_ICON_PATH), size=ICON_SIZE)
STOP_ICON = customtkinter.CTkImage(Image.open(STOP_ICON_PATH), size=ICON_SIZE)
CLIP_ICON = customtkinter.CTkImage(Image.open(CLIP_ICON_PATH), size=ICON_SIZE)
CLEAR_ICON = customtkinter.CTkImage(Image.open(CLEAR_ICON_PATH), size=ICON_SIZE)

class ClipWtApp:

    def __init__(self, controller) -> None:
        self._controller = controller
        self._model = controller._model
        self._init_ui()

    def _init_ui(self):
        self._window = customtkinter.CTk()
        self._window.title("📋 - ClipWt")
        self._window.resizable(width=False, height=False)
        self._window.geometry("350x425")
        self._window.attributes('-topmost', 'true')

        self._init_top_buttons()
        self._init_clipboard_storage()
        self._init_bottom_buttons()

    def _init_top_buttons(self):
        btn_frame = customtkinter.CTkFrame(master=self._window)
        btn_frame.pack()

        self._state_btn = customtkinter.CTkButton(master=btn_frame, image=PLAY_ICON,
                            text="", command=self.start_watching, border_color="red")
        self._state_btn.pack(expand=True, fill=tk.BOTH)

    def _init_clipboard_storage(self):
        clipboard_content = customtkinter.CTkFrame(master=self._window)
        clipboard_content.pack(fill=tk.X)

        self._text_box = customtkinter.CTkTextbox(clipboard_content, height=350)
        self._text_box.pack(expand=True, fill=tk.BOTH)

    def _init_bottom_buttons(self):
        btn_frame = customtkinter.CTkFrame(master=self._window)
        btn_frame.pack(fill=tk.X)
        
        btn_frame.rowconfigure(0, minsize=30, weight=1)
        btn_frame.columnconfigure([0, 1], minsize=30, weight=1)

        btn_select_all = customtkinter.CTkButton(master=btn_frame, image=CLIP_ICON, text="",
                             command=self.select_all)
        btn_select_all.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        btn_clear = customtkinter.CTkButton(master=btn_frame, image=CLEAR_ICON, text="",
                              command=self.clear_storage)
        btn_clear.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    def get_clipboard_content(self):
        try:
            clipboard_content = self._window.selection_get(selection="CLIPBOARD").strip()
        except:
            clipboard_content = ""

        self._controller.set_content(clipboard_content)

        if self._model.content:
            self._text_box.delete("0.0", tk.END)
            self._text_box.insert("0.0", self._model.content)
        
        if self._model.status == ClipAppStatus.START:
            self._text_box.after(1000, self.get_clipboard_content)

    def stop_watching(self):
        self._controller.stop_watching()
        self._state_btn.configure(image=PLAY_ICON, command=self.start_watching, border_width=0)

    def start_watching(self):
        self._window.clipboard_clear()
        self._state_btn.configure(image=STOP_ICON, command=self.stop_watching, border_width=2)
        self._controller.start_watching()
        self.get_clipboard_content()

    def clear_storage(self):
        self._controller.clear_storage()
        self._text_box.delete("0.0", tk.END)

    def select_all(self):
        self.stop_watching()
        self._window.clipboard_append(self._model.content)

    def show(self):
        self._window.mainloop()
