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
        while self.master.master.dirs == "wait":
            sleep(0.01)
        for directory in self.master.master.dirs: #master.master = gui
            localFrame = ctk.CTkFrame(self.dirbar, fg_color=['gray82', 'gray13'])
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

        self.dirbar.pack(side="left", padx=8, pady=8, fill="both", expand=True)
    
    def tweakClicked(self,directory,state,frame):
        path = abspath(join(self.master.master.basepath, directory, f"{directory}_{state}.bat"))
        print(f"Running |{path}|.")
        Popen([f'{path}'], shell=True)
        frame.nameLabel.configure(text_color="#" + ("aaff" if state == "on" else "ffaa") + "aa") #aaffaa for on, #ffaaaa for off