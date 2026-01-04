import customtkinter as ctk
from PIL import Image
from utils import resource_path
import threading
from os.path import basename
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import subprocess
import re

from pathlib import Path
DOWNLOADS_DIR = Path.home() / "Downloads"
class downloadsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master.main_area, fg_color="transparent")
        self.titleBar = ctk.CTkLabel(self, text="Downloads", font=ctk.CTkFont(size=32,weight="bold"), bg_color="#1d1a23", height=50)
        self.titleBar.pack(side="top", fill="x", pady=(0,5))
        data = {
            1: {
                "name": "Brave Browser",
                "size": 20,
                "link": "https://laptop-updates.brave.com/latest/winx64",
                "filename": "BraveBrowserSetup.exe",
                "requireVCheck": False
            },
            2: {
                "name": "Ungoogled Chromium",
                "size": 14,
                "link": "https://ungoogled-software.github.io/ungoogled-chromium-binaries/",
                "requireVCheck": True,
                "rules": {
                    "tag": "a",
                    "class": "td"
                }
            },
            3: {
                "name": "Tor Browser",
                "size": 20,
                "add": "https://www.torproject.org/",
                "link": "https://www.torproject.org/download/",
                "requireVCheck": True,
                "rules": {
                    "tag": "a",
                    "class": "btn btn-primary mt-4 downloadLink"
                }
            },
            4: {
                "name": "Firefox Browser",
                "size": 20,
                "link": "https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US",
                "filename": "Firefox Installer.exe",
                "requireVCheck": False
            },
            5: {
                "name": "Mullvad Browser",
                "size": 20,
                "link": "https://mullvad.net/en/download/browser/win64/latest",
                "filename": "Mullvad Browser.exe",
                "requireVCheck": False
            },
            6: {
                "name": "LibreWolf",
                "size": 20,
                "link": "run/choco install librewolf -y --force"
            },
            7: {
                "name": "Zen Browser",
                "size": 20,
                "link": "https://github.com/zen-browser/desktop/releases/latest/download/zen.installer.exe",
                "filename": "zen.installer.exe",
                "requireVCheck": False
            },
            8: {
                "name": "Discord",
                "size": 20,
                "link": "https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64",
                "filename": "DiscordSetup.exe",
                "requireVCheck": False
            },
            9: {
                "name": "Steam",
                "size": 20,
                "link": "https://cdn.fastly.steamstatic.com/client/installer/SteamSetup.exe",
                "filename": "SteamSetup.exe",
                "requireVCheck": False
            },
            10: {
                "name": "Free Download Manager",
                "size": 14,
                "link": "https://files2.freedownloadmanager.org/6/latest/fdm_x64_setup.exe",
                "filename": "fdm_x64_setup.exe",
                "requireVCheck": False
            },
            11: {
                "name": "qBittorrent",
                "size": 20,
                "link": "https://sourceforge.net/projects/qbittorrent/files/latest/download",
                "filename": "unknown", #placeholder name - gets replaced by latest ver name
                "requireVCheck": False
            }
        }
        self.scrollableDlFrame = ctk.CTkScrollableFrame(self, fg_color="#201d26")
        self.dlFrames = []
        for i,dl in enumerate(data):
            d = data[dl]
            row = i // 3
            col = i % 3


            dlFrame = ctk.CTkFrame(self.scrollableDlFrame, fg_color="#201d26")
            dlFrame.grid_propagate(False)
            dlFrame.configure(height=30)
            dlFrame.grid_columnconfigure(1, weight=1)

            dlLabel = ctk.CTkLabel(dlFrame, text=d["name"], font=ctk.CTkFont(size=d["size"]))
            dlLabel.grid_propagate(False)
            dlLabel.configure(width=150)
            dlLabel.grid(column=0,row=0, sticky="nsew", padx=(0,5))

            dlBtn = ctk.CTkButton(dlFrame, text="Download", font=ctk.CTkFont(size=16))
            dlBtn.configure(command=lambda b=dlBtn,f=dlFrame,d=d: self.download(b,f,d))
            dlBtn.grid(column=1,row=0, sticky="nsew")
            dlFrame.grid(column=col, row=row, padx=15, pady=9, sticky="nsew")
            self.dlFrames.append(dlFrame)
        self.scrollableDlFrame.pack(side="top", fill="both", expand=True)
        for c in range(3):
            self.scrollableDlFrame.grid_columnconfigure(c, weight=1)

    def download(self, btn, frame, data):
        btn.destroy()

        progressbar = ctk.CTkProgressBar(frame)
        progressbar.set(0)
        progressbar.grid(column=1, row=0, pady=3)

        name = data["name"]
        async def async_download():
            url = data["link"]
            if url.startswith("run/"): #install with cmd
                cmd = url[4:].split(" ")
                #chocolabel = ctk.CTkLabel(frame,text="Installing with chocolatey...")
                #chocolabel.grid(column=1,row=0,pady=3)
                #frame.grid_columnconfigure(1, weight=1)
                frame.grid_columnconfigure(1, weight=1)
                process = subprocess.Popen(cmd,stdout=subprocess.PIPE,text=True)
                path = "Completed"
                for line in process.stdout:
                    line = line.strip()
                    print(line)
                    if line.startswith("Progress: "):
                        matches = re.findall(r"\d+%",line)
                        p = int(matches[0][:-1])
                        progressbar.set(p/100)
                    elif line.startswith("Deployed to '"):
                        path = line.split("Deployed to '",1)[1].split("'",1)[0].replace("\"","")
                process.wait()
                self.after(0, lambda: self.completeDownload(progressbar,path)) #return to main thread for ui updates
            else:
                #handle qbittorrent separately
                if name == "qBittorrent":
                    curl1 = subprocess.Popen(["curl",data["link"]],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    stdout,stderr = curl1.communicate()
                    output = stdout.decode('utf-8')
                    url = BeautifulSoup(output,"html.parser").find("a")["href"]
                    data["filename"] = url.split("?ts=",1)[0].rsplit("/",1)[1]


                if data["requireVCheck"]:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url,timeout=aiohttp.ClientTimeout(total=60)) as resp:
                            resp.raise_for_status()
                            html = await resp.text()
                    soup = BeautifulSoup(html,"html.parser")
                    r = data["rules"]
                    
                    if name  == "Tor Browser":
                        link = soup.find(r["tag"],class_=r["class"])
                    elif name == "Ungoogled Chromium":
                        link = soup.find(r["tag"],href = lambda h: h and "/ungoogled-chromium-binaries/releases/windows/64bit/" in h)
                    url = link.get("href")
                    if not (link or href):
                        self.after(0, lambda: self.showError(progressbar,"link not found")) #return to main thread for ui updates
                        return
                    print(url)
                    if name  == "Tor Browser":
                        url = "https://www.torproject.org/" + url
                    elif name == "Ungoogled Chromium":
                        ver = url.rsplit("/",1)[1]
                        async with aiohttp.ClientSession() as session:
                            async with session.get("https://ungoogled-software.github.io/ungoogled-chromium-binaries/releases/windows/64bit/143.0.7499.169-1",timeout=aiohttp.ClientTimeout(total=60)) as resp:
                                resp.raise_for_status()
                                html = await resp.text()
                        soup2 = BeautifulSoup(html,"html.parser")
                        link = soup2.find(r["tag"],href = lambda h: h and "installer" in h)
                        url = link.get("href")
                    download_path = DOWNLOADS_DIR / url.rsplit("/",1)[1] #get correct filename
                else:
                    download_path = DOWNLOADS_DIR / data["filename"]
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        resp.raise_for_status()

                        total = resp.content_length or 0
                        downloaded = 0

                        with open(download_path, "wb") as f:
                            async for chunk in resp.content.iter_chunked(8192):
                                f.write(chunk)
                                downloaded += len(chunk)
                                if total:
                                    self.after(0, progressbar.set, downloaded / total)
                    self.after(0, lambda: self.completeDownload(progressbar,download_path)) #return to main thread for ui updates

        threading.Thread(target=lambda: asyncio.run(async_download()), daemon=True).start() #asynchronous download
    
    def completeDownload(self,progressbar,path):
        dlFrame = progressbar.master
        progressbar.destroy()
        dlFin = ctk.CTkLabel(dlFrame, text=path, font=ctk.CTkFont(size=9), text_color="#00ff00", justify="center", wraplength=150)
        dlFin.grid(column=1,row=0, sticky="nsew")
    
    def showError(self,progressbar,e):
        dlFrame = progressbar.master
        progressbar.destroy()
        dlErr = ctk.CTkLabel(dlFrame, text=f"Error, {e}", font=ctk.CTkFont(size=16), text_color="#ff0000", justify="center", wraplength=150)
        dlErr.grid(column=1,row=0, sticky="nsew")