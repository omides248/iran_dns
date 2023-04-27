import os

from tkinter import *

import pyuac

from config.config import Config
from lib.assets.image_icon import image_icon
from lib.download_version import DownloadVersion
from lib.frames.buttons_frame import ButtonsFrame
from lib.frames.footer_frame import FooterFrame
from lib.frames.interface_label_frame import InterfaceLabelFrame
from lib.frames.interface_option_frame import InterfaceOptionFrame
from lib.procss_handler import ProcessHandler

"""
pyinstaller --onefile --noconsole iran_dns.py
pyinstaller.exe --onefile --windowed --icon=iran_dns_icon.png iran_dns.py

pyinstaller.exe --onefile --windowed --icon=lib\assets\iran_dns_icon.ico iran_dns.py

netsh interface show interface
netsh interface ipv4 show config name="Wi-Fi"
netsh interface ipv4 show address "Wi-Fi"
netsh interface ipv4 show dnsservers name="Wi-Fi"

netsh interface ip set dnsservers name="Wi-Fi" source=dhcp
netsh interface ipv4 set dns name="Wi-Fi" static 178.22.122.100
netsh interface ipv4 set dns name="Wi-Fi" static 178.22.122.101 index=2



pip install pyuac
pip install pypiwin32


"""


class Windows:
    root_directory = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, master):
        self.master = master

        # init config
        master.title("IranDNS")
        master.rowconfigure(0, minsize=300, weight=1)
        master.columnconfigure(1, minsize=300, weight=1)
        master.iconphoto(True, PhotoImage(data=image_icon))

        self.frm_space1 = Frame(self.master, relief=RAISED, bd=0, background=Config.background_color)
        self.frm_space2 = Frame(self.master, relief=RAISED, bd=0, background=Config.background_color)
        self.frm_buttons = ButtonsFrame(self.master, self)
        self.frm_interface_option = InterfaceOptionFrame(self.master, self)
        self.frm_interface_label = InterfaceLabelFrame(self.master, self)
        self.frm_footer = FooterFrame(self.master, self)

        self.register_frame()

        from lib.profile import Profile
        if Profile().profile_interface_remember == 0:
            self.frm_buttons.disable_buttons()

        self.download_version()  # Check new version and download

    def download_version(self):
        d = DownloadVersion(self, self.master)
        d.download_new_version()

    def register_frame(self):
        self.frm_space1.pack(fill="both", expand=True, padx=80, pady=30)
        self.frm_buttons.pack(fill="both", expand=True, padx=100)
        self.frm_interface_option.pack()
        self.frm_interface_label.pack()
        self.frm_space2.pack(fill="both", expand=True, padx=100, pady=40)
        self.frm_footer.pack(side="bottom", fill="x", expand=True)


if __name__ == '__main__':
    try:
        if not ProcessHandler.windows_exists("IranDNS"):
            if not pyuac.isUserAdmin():
                pyuac.runAsAdmin()
            else:
                root = Tk()
                root.resizable(False, False)
                root.configure(background=Config.background_color)
                Windows(root)
                # root.attributes('-topmost', True)
                # root.update()
                root.mainloop()
    except Exception as e:
        print(e)
