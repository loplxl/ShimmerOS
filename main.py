#!/usr/bin/env python3
import customtkinter as ctk
ctk.set_appearance_mode("dark")
from sidebar import sidebar
from pages.homePage import homePage
from pages.downloadsPage import downloadsPage
from pages.tweaksPage import tweaksPage
from pages.toolsPage import toolsPage
from pages.quickaccessPage import quickaccessPage
from pages.aboutPage import aboutPage
from hashlib import sha256
import threading
import aiohttp
import asyncio
from datetime import datetime
from subprocess import Popen, DETACHED_PROCESS, CREATE_NEW_PROCESS_GROUP, CREATE_NO_WINDOW, PIPE
from os import listdir,getcwd,mkdir
from os.path import isdir,join,exists
createTweaks = False
#first check if tweaks tab should be made
drive = getcwd()[:2]
OSlivionP = join(drive,"/OSlivion/")
OSOP = join(OSlivionP,"OSO")
quickaccessP = join(OSOP,"quickaccess")
if not exists(OSlivionP):
    mkdir(OSlivionP)
if not exists(OSOP):
    mkdir(OSOP)
if not exists(quickaccessP):
    mkdir(quickaccessP)

if exists(drive + r"\OSlivion\OSO\Tweaks"):
    createTweaks = True
def closeAutoUpdater(self):
    print("close auto updater")
    self.updateTL.destroy()
class newGUI(ctk.CTk):

    async def AutoUpdater(self):
        print("Auto updater called")
        try:
            self.updateTL.attributes("-topmost", True)
            self.updateTL.after(10,lambda: self.updateTL.attributes("-topmost", False))
            print("Auto updater already exists, bringing to front.")
            return
        except Exception as e:
            print("No updater TL, creating...")
            self.updateTL = ctk.CTkToplevel(self, fg_color="#201d26")
            self.updateTL.protocol("WM_DELETE_WINDOW", lambda: closeAutoUpdater(self))
            self.updateTL.geometry("400x200")
            self.updateTL.title("Check for updates")

            self.processLabel = ctk.CTkTextbox(self.updateTL,fg_color="transparent")
            self.processLabel.configure(state="disabled")
            self.processLabel.pack(side="top",fill="x",expand=True, pady=5,padx=5)
            self.updateTL.attributes("-topmost", True)
            self.updateTL.after(10,lambda: self.updateTL.attributes("-topmost", False))
        def log(msg):
            self.processLabel.configure(state="normal")
            self.processLabel.insert("end", msg+"\n")
            self.processLabel.see("end")
            self.processLabel.configure(state="disabled")
            self.updateTL.update()

        log("Checking if update is required...")
        log("Current version: " + self.CurrentVersion)
        status = [0,0]
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.github.com/repos/loplxl/OSlivionOptions/releases/tags/" + self.CurrentVersion) as resp:
                    resp.raise_for_status()
                    jsonresp = await resp.json()
                    status[0] = jsonresp["updated_at"]
                async with session.get("https://api.github.com/repos/loplxl/OSlivionOptions/releases/latest") as resp2:
                    resp2.raise_for_status()
                    global jsonresp2
                    jsonresp2 = await resp2.json()
                    status[1] = jsonresp2["updated_at"]
        except Exception as e:
            log(f"Failed to get version info.\n{e}")
            return
        print(status)
        log(f"Current version update time: {status[0]}")
        log(f"Latest version update time: {status[1]}")

        current = datetime.fromisoformat(status[0].replace("Z", "+00:00"))
        latest  = datetime.fromisoformat(status[1].replace("Z", "+00:00"))

        if latest <= current:
            log("All up to date!")
            return
        log("Outdated OSO, updating...")
        log("Checking if auto updater is installed...")
        
        OSOUpdater_PATH = join(self.drive,"/Oslivion/OSOUpdater/OSOUpdater.exe")

        installed = False
        while not installed:
            install = False
            if not exists(OSOUpdater_PATH):
                log("Auto updater not installed. Installing...")
                install = True
            else:
                #check uncorrupted / latest version
                h256 = sha256()
                h256.update(open(OSOUpdater_PATH,'rb').read())
                hash = h256.hexdigest()
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get("https://api.github.com/repos/loplxl/OSOUpdater/releases/latest") as resp3:
                            resp3.raise_for_status()
                            OSOUresp = await resp3.json()
                except Exception as e:
                    log("Failed to hash OSOUpdater" + e)
                    return
                expectedhash = OSOUresp["assets"][0]["digest"][7:]
                log("Current: " + hash)
                log("Expected: " + expectedhash)
                if str(hash) != str(expectedhash):
                    log("Auto updater outdated or corrupted. Installing...")
                    install = True
                else:
                    log("Auto updater not corrupted and up to date, proceeding...")
                    break
            if install:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://github.com/loplxl/OSOUpdater/releases/latest/download/OSOUpdater.exe") as resp:
                        resp.raise_for_status()
                        with open(OSOUpdater_PATH, "wb") as f:
                            async for chunk in resp.content.iter_chunked(8192):
                                f.write(chunk)
            
            await asyncio.sleep(1) #wait 1s before loop to ensure everything is normal
        log("Auto updater is up to date")
        Popen(OSOUpdater_PATH.split(" "),creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,close_fds=True)
        on_close(self)

    def loadTweaks(self):
        self.basepath = self.drive + r"\Oslivion\OSO\Tweaks"
        self.dirs = sorted([d for d in listdir(self.basepath) if isdir(join(self.basepath,d))],key=str.casefold)

    def __init__(self):
        self.CurrentVersion = "1.2.0.1"
        self.dirs = "loading"
        self.drive = drive
        print(f"Running from drive {self.drive}")
        if createTweaks:
            threading.Thread(target=self.loadTweaks, daemon=True).start()


        super().__init__(fg_color="#201d26")
        self.openSubprocesses = []
        self.currentTab = "initialising"
        self.geometry("1200x650")
        self.title("OSlivion Options")
        self.cachedFrames = {
            "home": None,
            "downloads": None,
            "tweaks": None,
            "tools": None,
            "about": None
        }
        self.homePage_init()
        self.cachedFrames["home"] = self.main_area.page
        self.sb = sidebar(master=self,createTweaks=createTweaks)
        self.sb.pack(side="left", fill='y')
    
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
     
    def quickaccessPage_init(self):
        if self.currentTab != "quickaccess":
            self.currentTab = "quickaccess"
            # hide page
            for child in self.main_area.winfo_children():
                child.pack_forget()

            # show quickaccess page
            self.main_area.page = quickaccessPage(master=self)
            self.main_area.page.pack(side="right", fill="both", expand=True)

    def aboutPage_init(self):
        if self.currentTab != "about":
            self.currentTab = "about"
            # hide page
            for child in self.main_area.winfo_children():
                child.pack_forget()
            
            if self.cachedFrames["about"] is None:
                self.cachedFrames["about"] = aboutPage(master=self)
            
            # show about page
            self.main_area.page = self.cachedFrames["about"]
            self.main_area.page.pack(side="right", fill="both", expand=True)
    
def on_close(gui):
    try:
        gui.stop.set()
    except Exception:
        pass
    from subprocess import Popen, CREATE_NO_WINDOW
    apps = ["stress","MeasureSleep","timerres"]
    for app in apps:
        Popen(["taskkill","/f","/im",f"{app}.exe"],creationflags=CREATE_NO_WINDOW)
    for process in gui.openSubprocesses: #extra
        process.terminate()
    gui.destroy()
gui = newGUI()
gui.protocol("WM_DELETE_WINDOW", lambda: on_close(gui))
gui.mainloop()
