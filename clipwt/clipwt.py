import os
import tkinter as tk
from tkinter import *
from PIL import Image
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ressources")
PLAY_ICON = customtkinter.CTkImage(Image.open(os.path.join(image_path, "icon_play.png")), size=(16,16))
STOP_ICON = customtkinter.CTkImage(Image.open(os.path.join(image_path, "icon_stop.png")), size=(16,16))
CLEAR_ICON = customtkinter.CTkImage(Image.open(os.path.join(image_path, "icon_clear.png")), size=(16,16))

class ClipAppStatus:

    START = 0x1
    STOP = 0x11


class ClipWt:

    def __init__(self) -> None:
        self._last_content = None
        self._status = ClipAppStatus.STOP
        self._init_ui()

    def _init_ui(self):
        self._window = customtkinter.CTk()
        self._window.title("📋 - ClipWt")
        self._window.resizable(width=False, height=False)
        self._window.geometry("350x400")
        self._window.attributes('-topmost', 'true')

        self._init_buttons()
        self._init_clipboard_storage()

    def _init_buttons(self):
        btn_frame = customtkinter.CTkFrame(master=self._window)
        btn_frame.pack(fill=tk.X)
        
        btn_frame.rowconfigure(0, minsize=30, weight=1)
        btn_frame.columnconfigure([0, 1, 2], minsize=30, weight=1)

        btn_play = customtkinter.CTkButton(master=btn_frame, image=PLAY_ICON, text="",
                             command=self.start_watching)
        btn_play.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        btn_stop = customtkinter.CTkButton(master=btn_frame, image=STOP_ICON, text="",
                             command=self.stop_watching)
        btn_stop.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        btn_clear = customtkinter.CTkButton(master=btn_frame, image=CLEAR_ICON, text="",
                              command=self.clear_storage)
        btn_clear.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

    def _init_clipboard_storage(self):
        clipboard_content = customtkinter.CTkFrame(master=self._window)
        clipboard_content.pack(fill=tk.X)

        self._text_box = customtkinter.CTkTextbox(clipboard_content, height=350)
        self._text_box.pack(expand=True, fill=tk.BOTH)

    def get_clipboard_content(self):
    
        try:
            clipboard_content = self._window.selection_get(selection="CLIPBOARD").strip()
        except:
            clipboard_content = None

        storage_content = self._text_box.get("0.0", tk.END).strip()

        if storage_content:
            new_storage_value = f"{storage_content}\n{clipboard_content}"
        else:
            new_storage_value = f"{clipboard_content}"

        if clipboard_content != self._last_content:
            self._text_box.delete("0.0", tk.END)
            self._text_box.insert("0.0", new_storage_value)
            self._last_content = clipboard_content
        
        if self._status == ClipAppStatus.START:
            self._text_box.after(1000, self.get_clipboard_content)

    def stop_watching(self):
        self._status = ClipAppStatus.STOP

    def start_watching(self):
        self._window.clipboard_clear()
        self._status = ClipAppStatus.START
        self.get_clipboard_content()

    def save_storage(self):
        storage_content = self._text_box.get("0.0", tk.END).strip()
        self._window.clipboard_append(storage_content)

    def clear_storage(self):
        self._text_box.delete("0.0", tk.END)

    def show(self):
        self._window.mainloop()

def launch():
    app = ClipWt()
    app.show()