import webbrowser
from tkinter import *
from tkinter import ttk

from config.config import Config


class FooterFrame(Frame):
    def __init__(self, master, windows_main, **kwargs):
        super().__init__(master, **kwargs, relief=RAISED, bd=0, background=Config.background_color)

        self.master = master
        self.windows_main = windows_main

        self.update_lbl = ttk.Label(self, text="", foreground="green", background=Config.background_color)
        self.progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.telegram_lbl = ttk.Label(self, text="Telegram", foreground="blue", cursor="hand2",
                                      background=Config.background_color)
        self.github_lbl = ttk.Label(self, text="Github", foreground="blue", cursor="hand2",
                                    background=Config.background_color)
        self.version_lbl = ttk.Label(self, text=f"Version: {Config.version}",
                                     background=Config.background_color)

        # Footer Widget
        self.update_lbl.pack()
        self.progress.pack()
        self.telegram_lbl.pack()
        self.github_lbl.pack()
        self.version_lbl.pack()

        self.bind_widgets()

    def bind_widgets(self):
        self.telegram_lbl.bind("<Button-1>", lambda e: self.link_open_browser(Config.telegram_url))
        self.github_lbl.bind("<Button-1>", lambda e: self.link_open_browser(Config.github_url))

    @classmethod
    def link_open_browser(cls, url):
        webbrowser.open_new(url)
