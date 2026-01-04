from os.path import join,abspath
import sys
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # running as PyInstaller
        base_path = sys._MEIPASS
    else:
        base_path = abspath(".")
    return join(base_path, relative_path)