from config.config import Config
from tkinter import *
from tkinter import ttk


class SetDNSFrame(Frame):
    def __init__(self, master, windows_main, **kwargs):
        super().__init__(master, **kwargs, relief=RAISED, bd=0, background=Config.background_color)

        self.master = master
        self.windows_main = windows_main

        from lib.profile import Profile
        profile = Profile.read()

        self.set_dns_1_var = IntVar(self.master, value=profile.get("set_dns_1"))
        self.set_dns_2_var = IntVar(self.master, value=profile.get("set_dns_2"))

        self.set_dns_1 = ttk.Checkbutton(self, text="Dns 1", onvalue=1, offvalue=0,
                                         variable=self.set_dns_1_var,
                                         command=self.profile_set_dns_1_handler
                                         )
        self.set_dns_2 = ttk.Checkbutton(self, text="Dns 2", onvalue=1, offvalue=0,
                                         variable=self.set_dns_2_var,
                                         command=self.profile_set_dns_2_handler
                                         )

        # self.set_dns_1.grid(row=0, column=1, sticky="ew", padx=0, pady=0)
        # self.set_dns_2.grid(row=0, column=2, sticky="ew", padx=0, pady=0)

    def profile_set_dns_1_handler(self):
        from lib.profile import Profile
        Profile.insert(set_dns_1=self.set_dns_1_var.get())

    def profile_set_dns_2_handler(self):
        from lib.profile import Profile
        Profile.insert(set_dns_2=self.set_dns_2_var.get())
