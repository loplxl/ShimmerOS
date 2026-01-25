import logging
from datetime import datetime, timezone
import sys
from os import getcwd, path, mkdir
from customtkinter import CTk
DRIVE = getcwd()[:3]
LOGS_DIR = path.join(DRIVE, "Shimmer", "Software", "logging", "logs")
DEPENDS = [path.join(DRIVE, "Shimmer"), path.join(DRIVE, "Shimmer", "Software"), path.join(DRIVE, "Shimmer", "Software", "logging"), LOGS_DIR]
for directory in DEPENDS:
    if not path.exists(directory):
        mkdir(directory)
class ConsoleLogger:
    def __init__(self, log_filename=f"{LOGS_DIR}\\{round(datetime.now(timezone.utc).timestamp())}_log.txt",master=CTk):
        self.logger = logging.getLogger('ConsoleLogger')
        self.master = master
        self.logs = ""
        
        self.logger.setLevel(logging.DEBUG)
        log_handler = logging.FileHandler(log_filename)
        log_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)
        sys.stdout = self

    def write(self, message):
        if message.strip():
            self.logger.info(message.strip())
            self.logs += message.strip() + "\n"
            try:
                if self.master.logsTL.winfo_exists():
                    self.master.logsTL.logbox.configure(state="normal")
                    self.master.logsTL.logbox.insert("end", self.logs)
                    self.master.logsTL.logbox.see("end")
                    self.master.logsTL.logbox.configure(state="disabled")
            except Exception:
                pass

    def flush(self):
        pass


if __name__ == '__main__':
    logger = ConsoleLogger()
    print("log")
    print("ainhweubyfdainwue")
    print("ainhweubyfdai23436234c6v 34nwue")