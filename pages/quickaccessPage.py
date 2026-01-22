import customtkinter as ctk
from os import getcwd,listdir,mkdir
from os.path import join,exists
from subprocess import Popen, DETACHED_PROCESS, CREATE_NEW_PROCESS_GROUP

names = {
    "autoruns.exe": ("Autoruns",22),
    "GoInterruptPolicy.exe": ("GoInterruptPolicy",20),
    "NSudo.exe": ("NSudo",22)
}

class quickaccessPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master.main_area, fg_color="transparent")
        self.titleBar = ctk.CTkLabel(self, text="Quick Access", font=ctk.CTkFont(size=32,weight="bold"), bg_color="#1d1a23", height=50)
        self.titleBar.pack(side="top", fill="x", pady=(0,5))
        folderLoc = join(getcwd()[:2] + "\\","Oslivion","OSO","quickaccess")
        if not exists(folderLoc):
            mkdir(folderLoc)
            downloadedApps = []
        else:
            downloadedApps = listdir(folderLoc)
        if not len(downloadedApps):
            noticeLabel = ctk.CTkLabel(self, text="You don't have any quick access apps downloaded.\nDownload some from the downloads tab and come back!", font=ctk.CTkFont(size=26))
            noticeLabel.pack(side="top",pady=(8,0))
            return

        launchFrame = ctk.CTkFrame(self, fg_color="transparent")
        for index,app in enumerate(downloadedApps):
            row = index // 4 + 1
            column = index % 4
            appFrame = ctk.CTkFrame(launchFrame)
            appFrame.grid_propagate(False)
            appFrame.configure(height=40,width=220)

            appFrame.grid_columnconfigure(0, weight=1)
            appFrame.grid_rowconfigure(0, weight=1)

            data = names[app] #data[0] is name to display, data[1] is the size of font
            appDownloadButton = ctk.CTkButton(appFrame, text=data[0], width=90, font=ctk.CTkFont(size=data[1]))
            appDownloadButton.configure(command=lambda app=app: Popen([f"{folderLoc}\\{app}"],creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP))
            appDownloadButton.grid(row=0,column=0,sticky="nsew")
            appFrame.grid(row=row,column=column,padx=5,pady=5,sticky="ew")
        launchFrame.pack()
