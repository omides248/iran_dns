from tkinter import *
from tkinter import ttk

from config.config import Config
from lib.netsh import Netsh


class InterfaceOptionFrame(Frame):
    def __init__(self, master, windows_main, **kwargs):
        super().__init__(master, **kwargs, relief=RAISED, bd=0, background=Config.background_color)

        self.master = master
        self.windows_main = windows_main

        from lib.profile import Profile
        profile = Profile.read()

        self.interface_option = ["Select Your Internet", "Auto Detect"] + Netsh.get_all_interface_name()
        self.interface_var = StringVar(self.master, value=profile.get("interface_option_menu_choice"))
        self.remember_var = IntVar(self.master, value=profile.get("profile_interface_remember"))
        self.popup_menu = ttk.OptionMenu(self, self.interface_var,
                                         profile.get("interface_option_menu_choice"),
                                         *self.interface_option, command=self.option_changed)

        self.save_profile_chb = ttk.Checkbutton(self, text="Remember Internet", onvalue=1, offvalue=0,
                                                variable=self.remember_var,
                                                command=self.profile_checkbox_handler
                                                )

        self.save_profile_chb.grid(row=5, column=0, sticky="ew", padx=5, pady=0)
        self.popup_menu.grid(row=6, column=0, sticky="ew", padx=5, pady=0)

    def profile_checkbox_handler(self):
        from lib.profile import Profile
        Profile.insert(profile_interface_remember=self.remember_var.get(), interface_option=self.interface_var.get())

    def option_changed(self, *args):
        from lib.profile import Profile
        Profile.insert(interface_option=self.interface_var.get())
        if self.interface_var.get() == "Auto Detect" or self.interface_var.get() == "":
            self.windows_main.frm_buttons.interface_name = Netsh.get_default_interface_name()
        else:
            self.windows_main.frm_buttons.interface_name = self.interface_var.get()
        self.windows_main.frm_interface_label.update_frame_label()
