import os
import sys

import psutil
import win32ui


class ProcessHandler:

    @classmethod
    def kill_process_by_name(cls, proc_name=None):
        if not proc_name:
            proc_name = os.path.basename(sys.argv[0])

        for proc in psutil.process_iter():
            if proc.name() == proc_name:
                p = psutil.Process(proc.pid)
                p.terminate()

    @classmethod
    def exists_already_process(cls, proc_name=None):
        if not proc_name:
            proc_name = os.path.basename(sys.argv[0])

        for proc in psutil.process_iter():
            if proc.name() == proc_name:
                return True
        return False

    @classmethod
    def windows_exists(cls, appname=None):
        if appname:
            try:
                win32ui.FindWindow(None, appname)
            except win32ui.error:
                return False
            else:
                return True
