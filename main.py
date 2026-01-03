#!/usr/bin/env python3
import customtkinter as ctk
ctk.set_appearance_mode("dark")
from sidebar import sidebar
from homePage import homePage
from downloadsPage import downloadsPage
from tweaksPage import tweaksPage
<<<<<<< HEAD
=======
from toolsPage import toolsPage
>>>>>>> 6ef9f89 (add auto timer res)
from aboutPage import aboutPage

from os import listdir
from os.path import isdir,join,abspath
from utils import resource_path #used to find files built into exe / in the current dir
class newGUI(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="#201d26")
<<<<<<< HEAD
=======
        self.ATRtoplevel = False
>>>>>>> 6ef9f89 (add auto timer res)
        self.currentTab = "initialising"
        self.geometry("1200x650")
        self.title("OSlivion Options")
        self.cachedFrames = {
            "home": None,
            "downloads": None,
            "tweaks": None,
<<<<<<< HEAD
=======
            "tools": None,
>>>>>>> 6ef9f89 (add auto timer res)
            "about": None
        }
        self.homePage_init()
        self.cachedFrames["home"] = self.main_area.page
        self.dirs = "wait"
        self.sb = sidebar(master=self)
        self.sb.pack(side="left", fill='y')

        #load dirs for tweaks tab here to save time loading tweaks page - it is extremely unlikely that there will be a new tweak made during system uptime
        self.basepath = "C:\\PostInstall\\Tweaks"
        self.dirs = sorted([d for d in listdir(self.basepath) if isdir(join(self.basepath,d))],key=str.casefold)
    
    def homePage_init(self):
        if self.currentTab != "home":
            if self.currentTab == "initialising":
                self.main_area = ctk.CTkFrame(self, fg_color="transparent")
                self.main_area.pack(side="right", fill="both", expand=True)
            self.currentTab = "home"
            # hide page 
            for child in self.main_area.winfo_children():
                child.pack_forget()

            if self.cachedFrames["home"] is None:
                self.cachedFrames["home"] = homePage(master=self)

            # show home page
            self.main_area.page = self.cachedFrames["home"]
            self.main_area.page.pack(side="right", fill="both", expand=True)

    def downloadsPage_init(self):
        if self.currentTab != "downloads":
            self.currentTab = "downloads"
            # hide page
            for child in self.main_area.winfo_children():
                child.pack_forget()
            
            if self.cachedFrames["downloads"] is None:
                self.cachedFrames["downloads"] = downloadsPage(master=self)
            
            # show downloads page
            self.main_area.page = self.cachedFrames["downloads"]
            self.main_area.page.pack(side="right", fill="both", expand=True)
    
    def tweaksPage_init(self):
        if self.currentTab != "tweaks":
            self.currentTab = "tweaks"

            # hide page
            for child in self.main_area.winfo_children():
                child.pack_forget()

            if self.cachedFrames["tweaks"] is None:
                self.cachedFrames["tweaks"] = tweaksPage(master=self)
            
            # show tweaks page
            self.main_area.page = self.cachedFrames["tweaks"]
            self.main_area.page.pack(side="right", fill="both", expand=True)
<<<<<<< HEAD
=======
    
    def toolsPage_init(self):
        if self.currentTab != "tools":
            self.currentTab = "tools"
            # hide page
            for child in self.main_area.winfo_children():
                child.pack_forget()
            
            if self.cachedFrames["tools"] is None:
                self.cachedFrames["tools"] = toolsPage(master=self)
            
            # show tools page
            self.main_area.page = self.cachedFrames["tools"]
            self.main_area.page.pack(side="right", fill="both", expand=True)
>>>>>>> 6ef9f89 (add auto timer res)

    def aboutPage_init(self):
        if self.currentTab != "about":
            self.currentTab = "about"
            # hide page
            for child in self.main_area.winfo_children():
                child.pack_forget()
<<<<<<< HEAD
            
=======
                
>>>>>>> 6ef9f89 (add auto timer res)
            if self.cachedFrames["about"] is None:
                self.cachedFrames["about"] = aboutPage(master=self)
            
            # show about page
            self.main_area.page = self.cachedFrames["about"]
            self.main_area.page.pack(side="right", fill="both", expand=True)
gui = newGUI()
<<<<<<< HEAD
gui.mainloop()
=======
gui.mainloop()
print("gui dead, ensure timer res executables arent running")
from subprocess import Popen
apps = ["stress","MeasureSleep","timerres"]
for app in apps:
    Popen(["taskkill","/f","/im",f"{app}.exe"])
>>>>>>> 6ef9f89 (add auto timer res)
