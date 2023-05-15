from tkinter import *
from tkinter import ttk

from config.config import Config
from lib.enum.enum import DnsName, DnsIP
from lib.netsh import Netsh


class InterfaceLabelFrame(Frame):
    def __init__(self, master, windows_main, **kwargs):
        super().__init__(master, **kwargs, relief=RAISED, bd=0, background=Config.background_color)

        self.master = master
        self.windows_main = windows_main

        self.interface_name_lbl = ttk.Label(self, background=Config.background_color,
                                            foreground=Config.foreground_color, font=('Bold', 10, 'bold'))

        self.primary_dns_lbl = ttk.Label(self, text="", background=Config.background_color,
                                         foreground=Config.foreground_color, font=('Bold', 10, 'bold'))
        self.secondary_dns_lbl = ttk.Label(self, text="", background=Config.background_color,
                                           foreground=Config.foreground_color, font=('Bold', 10, 'bold'))

        self.update_frame_label()

        self.interface_name_lbl.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.primary_dns_lbl.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.secondary_dns_lbl.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

    def update_frame_label(self):
        interface_name = self.windows_main.frm_interface_option.interface_var.get()
        if interface_name == "Select Your Internet":
            self.windows_main.frm_buttons.disable_buttons()
        else:
            self.windows_main.frm_buttons.enable_buttons()

        if interface_name == "Auto Detect":
            interface_name = Netsh.get_default_interface_name()

        primary_dns, secondary_dns = Netsh.get_primary_secondary_dns(interface_name)

        d1 = f"DNS 1: {primary_dns}" if primary_dns else primary_dns
        d2 = f"DNS 2: {secondary_dns}" if secondary_dns else secondary_dns
        self.primary_dns_lbl.config(text=d1)
        self.secondary_dns_lbl.config(text=d2)

        if primary_dns == "" and secondary_dns == "":
            self.interface_name_lbl.config(text="")

        elif primary_dns in (DnsIP.radar_game_dns[0], DnsIP.radar_game_dns[1]) or secondary_dns in (
                DnsIP.radar_game_dns[0], DnsIP.radar_game_dns[1]):
            self.interface_name_lbl.config(text=f"{interface_name.strip()}: {DnsName.radar_game_txt}")

        elif primary_dns in (DnsIP.electro_dns[0], DnsIP.electro_dns[1]) or secondary_dns in (
                DnsIP.electro_dns[0], DnsIP.electro_dns[1]):
            self.interface_name_lbl.config(text=f"{interface_name.strip()}: {DnsName.electro_txt}")

        elif primary_dns in (DnsIP.d_403_online_dns[0], DnsIP.d_403_online_dns[1]) or secondary_dns in (
                DnsIP.d_403_online_dns[0], DnsIP.d_403_online_dns[1]):
            self.interface_name_lbl.config(text=f"{interface_name.strip()}: {DnsName.d_403_online_txt}")

        elif primary_dns in (DnsIP.shecan_dns[0], DnsIP.shecan_dns[1]) or secondary_dns in (
                DnsIP.shecan_dns[0], DnsIP.shecan_dns[1]):
            self.interface_name_lbl.config(text=f"{interface_name.strip()}: {DnsName.shecan_txt}")
