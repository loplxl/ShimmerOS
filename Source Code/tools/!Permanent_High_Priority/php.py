import customtkinter as ctk
import threading
import asyncio
import winreg
import psutil
REG_PATH = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options"
def on_close(self):
    print("close PHPtoplevel")
    self.PHPtoplevel.destroy()
def apply(self,value="default"):
    createnewtl = False
    try:
        if not self.PHPtoplevel.winfo_exists():
            createnewtl = True
    except Exception:
        createnewtl = True
    if createnewtl:
        self.PHPtoplevel = ctk.CTkToplevel(self, fg_color="#201d26")
        self.PHPtoplevel.protocol("WM_DELETE_WINDOW", lambda: on_close(self))
        self.PHPtoplevel.geometry("400x200")
        self.PHPtoplevel.title("Permanent High Priority")
        instructionsLabel = ctk.CTkLabel(self.PHPtoplevel,text="Select an executable to " + ("permanently set to high priority." if value == "default" else "revert high priority on."),wraplength=395,cursor="hand2")
        instructionsLabel.pack(side="top",pady=8)
        async def pick(label):
            try:
                EXE = ctk.filedialog.askopenfilename(title="Select the executable to modify",filetypes=[("Executable files", "*.exe")]).rsplit("/",1)[1]
                if not EXE:
                    return
                print(f"Selected EXE: {EXE}")
                PATH = f"{REG_PATH}\\{EXE}\\PerfOptions"
                REG_KEY = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, PATH)
                if value == "default":
                    winreg.SetValueEx(REG_KEY, "CpuPriorityClass", 0, winreg.REG_DWORD, 3)
                else:
                    winreg.DeleteValue(REG_KEY, "CpuPriorityClass")
                print(f"Set {EXE} to high CPU and IO priority.")
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if proc.info['name'].lower() == EXE.lower():
                            psutil.Process(proc.info['pid']).nice(psutil.HIGH_PRIORITY_CLASS if value == "default" else psutil.NORMAL_PRIORITY_CLASS)
                    except Exception as e:
                        print(f"Error setting priority for {EXE}: {e}")
                label.configure(text="Applied!")
                winreg.CloseKey(REG_KEY)
            except Exception as e:
                print(f"Unexpected error occured: {e}")
                statusLabel.configure(text=f"Unexpected error occured: {e}")
            self.PHPtoplevel.attributes("-topmost", True)
            self.PHPtoplevel.after(10,lambda: self.PHPtoplevel.attributes("-topmost", False))
        statusLabel = ctk.CTkLabel(self.PHPtoplevel,text="",font=ctk.CTkFont(size=20),wraplength=380)
        statusLabel.pack(side="top",pady=8)
        btn = ctk.CTkButton(self.PHPtoplevel,text="Select Executable",command=lambda: threading.Thread(target=lambda: asyncio.run(pick(statusLabel)), daemon=True).start())
        btn.pack(side="top",pady=8)
    self.PHPtoplevel.attributes("-topmost", True)
    self.PHPtoplevel.after(10,lambda: self.PHPtoplevel.attributes("-topmost", False))

def default(self,btn):
    apply(self, "delete")