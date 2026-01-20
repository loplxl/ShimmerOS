import customtkinter as ctk
from os.path import join,abspath
from subprocess import Popen
from time import sleep
class tweaksPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master.main_area, fg_color="transparent")
        self.titleBar = ctk.CTkLabel(self, text="Tweaks", font=ctk.CTkFont(size=32,weight="bold"), bg_color="#1d1a23", height=50)
        self.titleBar.pack(side="top", fill="x")

        #create scrollable sidebar frame to display all the dirs
        self.dirbar = ctk.CTkScrollableFrame(self, fg_color="#232029")
        r=0
        c=0
        frames = []
        while not master.dirs or master.dirs == "loading":
            sleep(0.01)
        for directory in master.dirs:
            print(directory)
            localFrame = ctk.CTkFrame(self.dirbar)
            localFrame.nameLabel = ctk.CTkLabel(localFrame, text=directory, font=ctk.CTkFont(size=24))
            localFrame.nameLabel.pack(side="left", padx=[10,0], pady=10)

            localFrame.onButton = ctk.CTkButton(localFrame, text="ON", fg_color="#477843", hover_color="#376833", command=lambda d=directory, f=localFrame: self.tweakClicked(d,"on",f), width=100, font=ctk.CTkFont(size=16))
            localFrame.offButton = ctk.CTkButton(localFrame, text="OFF", fg_color="#784343", hover_color="#683333", command=lambda d=directory, f=localFrame: self.tweakClicked(d,"off",f), width=100, font=ctk.CTkFont(size=16))

            localFrame.offButton.pack(side="right",padx=8)
            localFrame.onButton.pack(side="right",padx=8)

            localFrame.grid(row=r, column=c, sticky="nsew", padx=3, pady=6)
            self.dirbar.grid_columnconfigure(c, weight=1)
            c += 1
            if c > 1:
                c = 0
                r += 1

        warningFrame = ctk.CTkFrame(self, fg_color="#232029")
        warningLabel1 = ctk.CTkLabel(warningFrame,text="⚠️ WARNING ⚠️",font=ctk.CTkFont(size=32))
        warningLabel1.pack(side="top",pady=(100,0))
        warningLabel2 = ctk.CTkLabel(warningFrame,text="Do not blindly apply tweaks that you dont know what they do. Only follow official guides.\nWe are not responsible for any damage (however unlikely) you cause upon yourself.",font=ctk.CTkFont(size=22))
        warningLabel2.pack(side="top",pady=(15,0))
        def proceed():
            warningFrame.destroy()
            self.dirbar.pack(side="left", padx=8, pady=8, fill="both", expand=True)
        proceedBtn = ctk.CTkButton(warningFrame,text="I understand the risks",fg_color="#33ff33",hover_color="#00ff00",command=proceed,text_color="#000000")
        proceedBtn.pack(side="top",pady=25)
        returnBtn = ctk.CTkButton(warningFrame,text="Return Home",fg_color="#ff3333",hover_color="#ff0000",command=self.master.master.homePage_init,text_color="#000000")
        returnBtn.pack(side="top",pady=(50,25))
        warningFrame.pack(fill="both",expand=True)
    
    def tweakClicked(self,directory,state,frame):
        path = abspath(join(self.basepath, directory, f"{directory}_{state}.bat"))
        print(f"Running |{path}|.")
        Popen([f'{path}'], shell=True)
        frame.nameLabel.configure(text_color="#" + ("aaff" if state == "on" else "ffaa") + "aa") #aaffaa for on, #ffaaaa for off