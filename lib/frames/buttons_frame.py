from threading import Thread
from tkinter import *
from tkinter import ttk

from config.config import Config
from lib.enum.enum import DnsIP, DnsName
from lib.netsh import Netsh


class ButtonsFrame(Frame):
    def __init__(self, master, windows_main, **kwargs):
        super().__init__(master, **kwargs, relief=RAISED, bd=0, background=Config.background_color)

        self.master = master
        self.windows_main = windows_main

        self.allow_click_electro_btn = True
        self.allow_click_radar_game_btn = True
        self.allow_click_403_online_btn = True
        self.allow_click_shecan_btn = True
        self.allow_click_remove_btn = True
        self.interface_name = self.get_interface_name_base_profile()

        self.btn_electro_dns = ttk.Button(self, text=DnsName.electro_txt, command=self.handle_click_electro)
        self.btn_radar_game_dns = ttk.Button(self, text=DnsName.radar_game_txt, command=self.handle_click_radar_game)
        self.btn_403_online_dns = ttk.Button(self, text=DnsName.d_403_online_txt, command=self.handle_click_403_online)
        self.btn_shecan_dns = ttk.Button(self, text=DnsName.shecan_txt, command=self.handle_click_shecan)
        self.btn_remove = ttk.Button(self, text="Remove", command=self.handle_click_remove)

        # Footer Widget
        self.btn_electro_dns.grid(row=0, column=0, sticky="ew", padx=5, pady=3)
        self.btn_radar_game_dns.grid(row=1, column=0, sticky="ew", padx=5, pady=3)
        self.btn_shecan_dns.grid(row=2, column=0, sticky="ew", padx=5, pady=3)
        self.btn_403_online_dns.grid(row=3, column=0, sticky="ew", padx=5, pady=3)
        self.btn_remove.grid(row=4, column=0, sticky="ew", padx=5, pady=15)

    def set_electro_dns(self):
        print("Electro")
        self.allow_click_electro_btn = False
        self.disable_buttons()

        primary_dns, secondary_dns = self.get_primary_secondary_dns_base_profile(DnsName.electro_txt)
        Netsh.set_dns(self.interface_name, primary_dns, secondary_dns)

        self.windows_main.frm_interface_label.update_frame_label()

        self.allow_click_electro_btn = True
        self.enable_buttons()
        print("Electro end set  DNS")

    def set_radar_game_dns(self):
        print("Radar Game")
        self.allow_click_radar_game_btn = False
        self.disable_buttons()

        primary_dns, secondary_dns = self.get_primary_secondary_dns_base_profile(DnsName.radar_game_txt)
        Netsh.set_dns(self.interface_name, primary_dns, secondary_dns)

        self.windows_main.frm_interface_label.update_frame_label()

        self.allow_click_radar_game_btn = True
        self.enable_buttons()
        print("Radar Game end set  DNS")

    def set_403_online_dns(self):
        print("403.online")
        self.allow_click_403_online_btn = False
        self.disable_buttons()

        primary_dns, secondary_dns = self.get_primary_secondary_dns_base_profile(DnsName.d_403_online_txt)
        Netsh.set_dns(self.interface_name, primary_dns, secondary_dns)

        self.windows_main.frm_interface_label.update_frame_label()

        self.allow_click_403_online_btn = True
        self.enable_buttons()
        print("403.online end set DNS")

    def set_shecan_dns(self):
        print("Shecan")
        self.allow_click_shecan_btn = False
        self.disable_buttons()

        primary_dns, secondary_dns = self.get_primary_secondary_dns_base_profile(DnsName.shecan_txt)
        Netsh.set_dns(self.interface_name, primary_dns, secondary_dns)

        self.windows_main.frm_interface_label.update_frame_label()

        self.allow_click_shecan_btn = True
        self.enable_buttons()
        print("shecan end set DNS")

    def remove_dns(self):
        print("Start Remove")
        self.allow_click_remove_btn = False
        self.disable_buttons()

        Netsh.clear_dns(self.interface_name)

        self.windows_main.frm_interface_label.update_frame_label()

        self.enable_buttons()
        self.allow_click_remove_btn = True
        print("End remove dns")

    @classmethod
    def get_interface_name_base_profile(cls):
        from lib.profile import Profile
        if Profile().interface_name == "Auto Detect" or Profile().interface_name == "":
            interface_name = Netsh.get_default_interface_name()
        else:
            interface_name = Profile().interface_name
        return interface_name

    @classmethod
    def get_primary_secondary_dns_base_profile(cls, dns_name=None):
        from lib.profile import Profile

        if dns_name:
            if dns_name == DnsName.electro_txt:
                primary_dns, secondary_dns = DnsIP.electro_dns
            elif dns_name == DnsName.radar_game_txt:
                primary_dns, secondary_dns = DnsIP.radar_game_dns
            elif dns_name == DnsName.shecan_txt:
                primary_dns, secondary_dns = DnsIP.shecan_dns
            elif dns_name == DnsName.d_403_online_txt:
                primary_dns, secondary_dns = DnsIP.d_403_online_dns
            else:
                primary_dns, secondary_dns = None, None

            set_dns_1 = Profile().set_dns_1
            set_dns_2 = Profile().set_dns_2

            if set_dns_1 == 0 and set_dns_2 == 0:
                primary_dns, secondary_dns = None, None
            elif set_dns_1 == 0 and set_dns_2 == 1:
                primary_dns = secondary_dns
                secondary_dns = None
            elif set_dns_1 == 1 and set_dns_2 == 0:
                secondary_dns = None

            return primary_dns, secondary_dns
        return None, None

    def handle_click_radar_game(self):
        if not self.allow_click_radar_game_btn:
            return
        t = Thread(target=self.set_radar_game_dns, daemon=True)
        t.start()
        self.master.after(5, self.check_thread, t)

    def handle_click_electro(self):
        if not self.allow_click_electro_btn:
            return
        t = Thread(target=self.set_electro_dns, daemon=True)
        t.start()
        self.master.after(5, self.check_thread, t)

    def handle_click_403_online(self):
        if not self.allow_click_403_online_btn:
            return
        t = Thread(target=self.set_403_online_dns, daemon=True)
        t.start()
        self.master.after(5, self.check_thread, t)

    def handle_click_shecan(self):
        if not self.allow_click_shecan_btn:
            return
        t = Thread(target=self.set_shecan_dns, daemon=True)
        t.start()
        self.master.after(5, self.check_thread, t)

    def handle_click_remove(self):
        if not self.allow_click_remove_btn:
            return
        t = Thread(target=self.remove_dns, daemon=True)
        t.start()
        self.master.after(5, self.check_thread, t)

    def check_thread(self, thread_obj):
        if thread_obj.is_alive():
            self.master.after(5, self.check_thread, thread_obj)

    def disable_buttons(self):
        self.btn_electro_dns.config(state="disabled")
        self.btn_radar_game_dns.config(state="disabled")
        self.btn_403_online_dns.config(state="disabled")
        self.btn_shecan_dns.config(state="disabled")
        self.btn_remove.config(state="disabled")

    def enable_buttons(self):
        self.btn_electro_dns.config(state="normal")
        self.btn_radar_game_dns.config(state="normal")
        self.btn_403_online_dns.config(state="normal")
        self.btn_shecan_dns.config(state="normal")
        self.btn_remove.config(state="normal")
