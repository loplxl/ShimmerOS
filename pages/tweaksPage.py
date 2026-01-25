import customtkinter as ctk
from os.path import join,abspath,exists
from os import listdir,getcwd
SOFTWARE_DIR = join(getcwd()[2:],"/Shimmer","Software")
from subprocess import Popen
from time import sleep
import json
class tweaksPage(ctk.CTkFrame):
    def rmbBind(self,widget,description,directory):
        widget.bind("<Button-3>",lambda e: self.helpbox(description,directory))
        for child in widget.winfo_children():
            self.rmbBind(child, description, directory)
    helpTLs = {}
    def helpbox(self, description, directory):
        if directory in self.helpTLs:
            helpTL = self.helpTLs[directory]
            helpTL.attributes("-topmost", True)
            helpTL.after(10,lambda: helpTL.attributes("-topmost", False))
            print("TL already open, taking top")
            return
        print("Creating new TL")
        helpTL = ctk.CTkToplevel(self, fg_color="#201d26")
        helpTL.geometry("400x200")
        helpTL.title(directory)
        def on_close(d=directory):
            if d in self.helpTLs:
                self.helpTLs[d].destroy()
                del self.helpTLs[d]
        helpTL.protocol("WM_DELETE_WINDOW",on_close)
        self.helpTLs[directory] = helpTL
        helpLabel = ctk.CTkLabel(helpTL,text=description,wraplength=395)
        helpLabel.pack(side="top",fill="x")
        helpTL.attributes("-topmost", True)
        helpTL.after(10,lambda: helpTL.attributes("-topmost", False))
    def __init__(self, master):
        super().__init__(master=master.main_area, fg_color="transparent")
        self.titleBar = ctk.CTkLabel(self, text="Tweaks", font=ctk.CTkFont(size=32,weight="bold"), bg_color="#1d1a23", height=50)
        self.titleBar.pack(side="top", fill="x")

        #create scrollable sidebar frame to display all the dirs
        warningFrame = ctk.CTkFrame(self, fg_color="#232029")
        warningLabel1 = ctk.CTkLabel(warningFrame,text="⚠️ WARNING ⚠️",font=ctk.CTkFont(size=32))
        warningLabel1.pack(side="top",pady=(45,0))
        warningLabel2 = ctk.CTkLabel(warningFrame,text="Do not blindly apply tweaks that you dont know what they do. Only follow official guides.\nWe are not responsible for any damage (however unlikely) you cause upon yourself.",font=ctk.CTkFont(size=22),wraplength=master.width/1250*950)
        warningLabel2.pack(side="top",pady=(15,0))
        def proceed():
            warningFrame.destroy()
            self.dirbar.pack(side="left", padx=8, pady=8, fill="both", expand=True)
        proceedBtn = ctk.CTkButton(warningFrame,text="I understand the risks",fg_color="#33ff33",hover_color="#00ff00",command=proceed,text_color="#000000")
        proceedBtn.pack(side="top",pady=25)
        returnBtn = ctk.CTkButton(warningFrame,text="Return Home",fg_color="#ff3333",hover_color="#ff0000",command=self.master.master.homePage_init,text_color="#000000")
        returnBtn.pack(side="top",pady=(10,25))
        warningFrame.pack(fill="both",expand=True)

        
        self.dirbar = ctk.CTkScrollableFrame(self, fg_color="#232029")
        r=0
        c=0
        while not master.dirs or master.dirs == "loading":
            sleep(0.01)
        for directory in master.dirs:
            filesdir = join(self.master.master.basepath,directory)
            print("Loading " + str(filesdir))
            files = listdir(filesdir)

            try:
                with open(join(filesdir,"help.json"),'r') as f:
                    helpdata = json.load(f)
                    description = helpdata["description"]
                    file = helpdata["target"]
            except Exception as e:
                file = str(e)

            try:
                with open(join(filesdir,"help.json"),'r') as f:
                    requirement = helpdata["requirement"]
            except Exception as e:
                requirement = None
            
            requirementNotMet = False
            if requirement == "nsudo" and not exists(join(SOFTWARE_DIR,"quickaccess","NSudo.exe")):
                requirementNotMet = True
            localFrame = ctk.CTkFrame(self.dirbar, cursor="hand2")
            localFrame.nameLabel = ctk.CTkLabel(localFrame, text=directory.replace("_"," "), font=ctk.CTkFont(size=24))
            localFrame.nameLabel.pack(side="left", padx=[10,0], pady=10)
            if requirementNotMet:
                localFrame.nameLabel.configure(text=f"not met requirement: {requirement} - download it in downloads page, then reopen app", font=ctk.CTkFont(size=13))
            else:
                if "on.bat" in files and "off.bat" in files:
                    localFrame.onButton = ctk.CTkButton(localFrame, text="ON", fg_color="#477843", hover_color="#376833", command=lambda d=directory, f=localFrame: self.ONOFFtweakClicked(d,"on",f), width=50, font=ctk.CTkFont(size=16))
                    localFrame.offButton = ctk.CTkButton(localFrame, text="OFF", fg_color="#784343", hover_color="#683333", command=lambda d=directory, f=localFrame: self.ONOFFtweakClicked(d,"off",f), width=50, font=ctk.CTkFont(size=16))
                    localFrame.offButton.pack(side="right",padx=8)
                    localFrame.onButton.pack(side="right",padx=8)
                    self.rmbBind(localFrame,description,join(filesdir,file))
                else:
                    if "action.bat" in files:
                        localFrame.onButton = ctk.CTkButton(localFrame, text="Apply", fg_color="#477843", hover_color="#376833", command=lambda d=directory, f=localFrame: self.SingleBattweakclicked(d,f), width=116, font=ctk.CTkFont(size=16))
                        localFrame.onButton.pack(side="right",padx=8)
                        self.rmbBind(localFrame,description,join(filesdir,file))
                    elif file.endswith(".reg"):
                        localFrame.regButton = ctk.CTkButton(localFrame, text=file.replace("_"," "), fg_color="#436A78", hover_color="#335A68", command=lambda d=join(filesdir,file), f=localFrame: self.regTweakClicked(d,f))
                        localFrame.regButton.pack(side="right",padx=8)
                        self.rmbBind(localFrame,description,join(filesdir,file))
                    elif file.endswith(".ps1"):
                        localFrame.regButton = ctk.CTkButton(localFrame, text=file.replace("_"," "), fg_color="#574378", hover_color="#473368", command=lambda d=join(filesdir,file), f=localFrame: self.ps1TweakClicked(d,f))
                        localFrame.regButton.pack(side="right",padx=8)
                        self.rmbBind(localFrame,description,join(filesdir,file))
                    else:
                        localFrame.errorLabel = ctk.CTkLabel(localFrame, text=file)
                        localFrame.errorLabel.pack(side="right",padx=8)
            localFrame.grid(row=r, column=c, sticky="nsew", padx=3, pady=6)
            self.dirbar.grid_columnconfigure(c, weight=1)
            master.shrink(localFrame.nameLabel, round((master.width/1250*1030-141)/2) - 116, 30)
            c += 1
            if c > 1:
                c = 0
                r += 1

        
    
    def ONOFFtweakClicked(self,directory,state,frame):
        path = abspath(join(self.master.master.basepath, directory, f"{state}.bat"))
        print(f"Running |{path}|.")
        Popen([f'{path}'], shell=True)
        frame.nameLabel.configure(text_color="#" + ("aaff" if state == "on" else "ffaa") + "aa") #aaffaa for on, #ffaaaa for off
    def regTweakClicked(self,directory,frame):
        print(f"Running |{directory}|.")
        Popen(["regedit","/s",directory], shell=True)
        frame.nameLabel.configure(text_color="#aaffaa")
    def ps1TweakClicked(self,directory,frame):
        print(f"Running |{directory}|.")
        cmd = ["powershell.exe", '-ExecutionPolicy', 'Unrestricted', directory]
        proc = Popen(cmd, shell=True)
        print(proc.returncode)
        frame.nameLabel.configure(text_color="#aaffaa")
    def SingleBattweakclicked(self,directory,frame):
        path = abspath(join(self.master.master.basepath, directory, f"action.bat"))
        print(f"Running |{path}|.")
        Popen([f'{path}'], shell=True)
        frame.nameLabel.configure(text_color="#aaffaa")
        