import customtkinter as ctk
from webbrowser import open as openLink
from os import path,getcwd,system,listdir,remove,rename,mkdir
from subprocess import Popen, DETACHED_PROCESS, CREATE_NEW_PROCESS_GROUP, PIPE
from shutil import rmtree
import threading
import asyncio
def on_close(self):
    print("close amdvddtoplevel")
    self.AMDVDDtoplevel.destroy()
def apply(self):
    createnewtl = False
    try:
        if not self.AMDVDDtoplevel.winfo_exists():
            createnewtl = True
    except Exception:
        createnewtl = True
    if createnewtl:
        self.AMDVDDtoplevel = ctk.CTkToplevel(self, fg_color="#201d26")
        self.AMDVDDtoplevel.protocol("WM_DELETE_WINDOW", lambda: on_close(self))
        self.AMDVDDtoplevel.geometry("400x150")
        self.AMDVDDtoplevel.title("AMD Video Driver Debloat")
        instructionsLabel = ctk.CTkLabel(self.AMDVDDtoplevel,text="Click this label to open AMD driver download page. Download your recommended driver (Adrenalin Edition needed) and then use the box below to point this tool to the executable.",wraplength=395,cursor="hand2")
        instructionsLabel.bind("<Button-1>", lambda e: openLink("https://www.amd.com/en/support/download/drivers.html#search-browse-drivers"))
        instructionsLabel.pack(side="top",pady="8")
        async def pick(statusLabel):
            try:
                EXE_PATH = ctk.filedialog.askopenfile(title="Select the AMD video Driver to debloat",filetypes=[("Executable files", "*.exe")])
                CLEAN_DIR = path.join(path.dirname(EXE_PATH.name),"SHIMMER_AMD_DEBLOAT")
                if path.exists(CLEAN_DIR):
                    rmtree(CLEAN_DIR)
                if not EXE_PATH:
                    return
                
                instructionsLabel.configure(text="Select which components to remove:")
                confframe = ctk.CTkFrame(self.AMDVDDtoplevel)

                amdocl = ctk.StringVar(value="amdocl")
                amdocl_cb = ctk.CTkCheckBox(confframe,text="AMDOCL\nNeeded for Adobe, Davinci, HandBrake, etc",variable=amdocl,onvalue="amdocl",offvalue="DISABLED")
                amdocl_cb.select()
                amdocl_cb.pack(side="top",padx=5,pady=5)

                amdpcibridge = ctk.StringVar(value="amdpcibridge")
                amdpcibridge_cb = ctk.CTkCheckBox(confframe,text="amdpcibridge\nAllows CPU to communicate with AXI based PCIe hardware",variable=amdpcibridge,onvalue="amdpcibridge",offvalue="DISABLED")
                amdpcibridge_cb.select()
                amdpcibridge_cb.pack(side="top",padx=5,pady=5)

                amdwin = ctk.StringVar(value="amdwin")
                amdwin_cb = ctk.CTkCheckBox(confframe,text="amdwin\nSpeeds up GPU frame capturing on Windows",variable=amdwin,onvalue="amdwin",offvalue="DISABLED")
                amdwin_cb.select()
                amdwin_cb.pack(side="top",padx=5,pady=5)

                amdxe = ctk.StringVar(value="amdxe")
                amdxe_cb = ctk.CTkCheckBox(confframe,text="amdxe\nUpdate checking and data tracking.",variable=amdxe,onvalue="amdxe",offvalue="DISABLED")
                amdxe_cb.select()
                amdxe_cb.pack(side="top",padx=5,pady=5)

                amdfdans = ctk.StringVar(value="amdfdans")
                amdfdans_cb = ctk.CTkCheckBox(confframe,text="amdfdans\nAMD Dynamic Audio Noise Suppression Service",variable=amdfdans,onvalue="amdfdans",offvalue="DISABLED")
                amdfdans_cb.select()
                amdfdans_cb.pack(side="top",padx=5,pady=5)

                amdfendr = ctk.StringVar(value="amdfendr")
                amdfendr_cb = ctk.CTkCheckBox(confframe,text="amdfendr\nAMD Crash Defender Service",variable=amdfendr,onvalue="amdfendr",offvalue="DISABLED")
                amdfendr_cb.select()
                amdfendr_cb.pack(side="top",padx=5,pady=5)
                self.AMDVDDtoplevel.geometry("400x335")
                confframe.pack(side="top",fill="both",expand=True)
                def cont():
                    self.after(0,confframe.destroy)
                    self.after(0,instructionsLabel.destroy)
                    self.after(0,btn.destroy)
                    EXTRACTED_DIR = path.join(path.dirname(EXE_PATH.name),"SHIMMER_AMD_DEBLOAT_TEMP")
                    command = f'"{path.join(getcwd()[:2],"/Program Files/","7-Zip/","7z.exe")}" x {EXE_PATH.name} -o{EXTRACTED_DIR} -y'
                    statusLabel.pack(side="top",pady=8)
                    statusLabel.configure(text="Extracting driver...")
                    self.AMDVDDtoplevel.attributes("-topmost", True)
                    self.AMDVDDtoplevel.after(10,lambda: self.AMDVDDtoplevel.attributes("-topmost", False))
                    system(command)
                    statusLabel.configure(text="Extracting complete\nDeleting unnecessary files...")
                    DRIVER_DIR = path.join(EXTRACTED_DIR,"Packages","Drivers","Display","WT6A_INF")
                    delete = [amdocl.get(),amdpcibridge.get(),amdwin.get(),amdxe.get(),amdfdans.get(),amdfendr.get()]
                    print(f"Deleting:\n{delete}")
                    mkdir(CLEAN_DIR)
                    global INF
                    INF = None
                    for dir in listdir(DRIVER_DIR):
                        print(f"Checking {dir}...")
                        if dir.endswith(".inf"):
                            INF = dir
                        elif dir in delete:
                            print(f"Deleting {dir}...\n")
                            if path.isdir(path.join(DRIVER_DIR,dir)):
                                rmtree(path.join(DRIVER_DIR,dir))
                            else:
                                remove(path.join(DRIVER_DIR,dir))
                            continue
                        print(f"Moving {dir}...\n")
                        rename(path.join(DRIVER_DIR,dir),path.join(CLEAN_DIR,dir))
                    if INF:
                        print("Debloat successful, installing driver")
                        statusLabel.configure(text="Debloat successful!\nInstalling new driver...\n\nThis may take ~15 seconds")
                        proc = Popen(["pnputil","/add-driver",path.join(CLEAN_DIR,INF),"/install"],creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,stdout=PIPE,stderr=PIPE,text=True,close_fds=True)
                        proc.wait()
                        if proc.returncode == 0:
                            statusLabel.configure(text="Successfully completed!")
                            rmtree(CLEAN_DIR)
                            remove(EXE_PATH.name)
                        else:
                            proc.communicate()
                            if proc.returncode == 5:
                                statusLabel.configure(text="Not admin")
                            if proc.returncode == 259:
                                statusLabel.configure(text="Better driver already installed\nuninstall the old one first.")
                            else:
                                statusLabel.configure(text=f"Failed with code {proc.returncode}")
                    else:
                        raise Exception("INF file not found")
                btn.configure(text="Confirm",command=lambda: threading.Thread(target=cont,daemon=True).start())
                self.AMDVDDtoplevel.attributes("-topmost", True)
                self.AMDVDDtoplevel.after(10,lambda: self.AMDVDDtoplevel.attributes("-topmost", False))
            except AttributeError: #user didnt select a driver
                pass
            except Exception as e:
                statusLabel.configure(text=f"Unexpected error occured: {e}")
        statusLabel = ctk.CTkLabel(self.AMDVDDtoplevel,text="",font=ctk.CTkFont(size=20),wraplength=380)
        btn = ctk.CTkButton(self.AMDVDDtoplevel,text="Select Driver",command=lambda: threading.Thread(target=lambda: asyncio.run(pick(statusLabel)), daemon=True).start())
        btn.pack(side="top",pady=8)
    self.AMDVDDtoplevel.attributes("-topmost", True)
    self.AMDVDDtoplevel.after(10,lambda: self.AMDVDDtoplevel.attributes("-topmost", False))
