import os
import sys
from threading import Thread

import requests

from config.config import Config
from lib.github_api import GithubAPI
from lib.procss_handler import ProcessHandler


class DownloadVersion:

    def __init__(self, windows_main, master):
        self.windows_main = windows_main
        self.master = master
        self.bytes = 0
        self.max_bytes = 0
        self.download_failed = False

    def download_new_version(self):

        tag_name, download_url, filename = GithubAPI.get_browser_download_url_latest_release()
        if tag_name and download_url and filename:
            if tag_name == Config.version:
                self.windows_main.frm_footer.update_lbl.config(text=f"You have latest version", foreground="green")
            else:
                from iran_dns import Windows
                local_directory = os.path.join(Windows.root_directory, "updates", tag_name)
                local_filename = os.path.join(local_directory, filename)
                try:
                    os.makedirs(local_directory, exist_ok=True)
                except Exception as e:
                    print(e)
                    return
                if not os.path.exists(local_filename):
                    self.windows_main.frm_footer.update_lbl.config(text=f"Downloading new version {tag_name}",
                                                                   foreground="green")
                    print("Download new version", tag_name)
                    Thread(target=self.download_file, args=(download_url, local_filename), daemon=True).start()
                else:
                    os.startfile(local_filename)
                    ProcessHandler.kill_process_by_name()
                    sys.exit(0)

    def read_bytes(self):
        if self.download_failed:
            return
        self.windows_main.frm_footer.progress["value"] = self.bytes
        if self.bytes < self.max_bytes:
            # read more bytes after 100 ms
            self.master.after(100, self.read_bytes)

    def download_file(self, url, local_filename_downloading):
        try:
            with requests.get(url, stream=True, timeout=10) as r:
                r.raise_for_status()
                local_filename_downloading = f"{local_filename_downloading}.downloading"
                cl_bytes = int(r.headers.get("Content-Length"))
                self.windows_main.frm_footer.progress["value"] = 0
                self.max_bytes = cl_bytes
                self.windows_main.frm_footer.progress["maximum"] = cl_bytes
                Thread(target=self.read_bytes, daemon=True).start()
                with open(local_filename_downloading, 'wb') as f:
                    chunk_size = 8192
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
                        self.bytes += chunk_size
                local_filename = str(local_filename_downloading).replace(".downloading", "")
                os.rename(local_filename_downloading, local_filename)
                self.windows_main.frm_footer.update_lbl.config(text="Download Complete", foreground="green")
                os.startfile(local_filename)
                ProcessHandler.kill_process_by_name()
                sys.exit(0)

        except Exception as e:
            print(e)
            self.windows_main.frm_footer.update_lbl.config(text=f"Error for downloading", foreground="red")
            self.download_failed = True
            return
