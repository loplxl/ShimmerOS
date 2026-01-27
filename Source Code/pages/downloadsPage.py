downloads = { #category / [name to display,module location,font size]
    "Shimmer quick access": [
        ["Autoruns","quickaccess.autoruns",20],
        ["GoInterruptPolicy","quickaccess.goip",15],
        ["$xNSudo","quickaccess.nsudo",22], #$x means that getURL is a procedure, not a function
        ["$xAuto Gpu Affinity","quickaccess.aga",14]
    ],
    "Firefox based browsers": [
        ["⭐ Tor","firefox.tor",22],
        ["⭐ Mullvad","firefox.mullvad",20],
        ["Zen","firefox.zen",22],
        ["Waterfox","firefox.waterfox",20],
        ["⭐ Firefox","firefox.firefox",20],
        ["Librewolf","firefox.librewolf",20],
        ["Floorp","firefox.floorp",20]
    ],
    "Chromium based browsers": [
        ["Google Chrome","chromium.chrome",18],
        ["⭐ Brave","chromium.brave",20],
        ["Vivaldi","chromium.vivaldi",20],
        ["Ungoogled\nChromium","chromium.ungoogled",14],
        ["⭐ Helium","chromium.helium",20],
        ["SRWare Iron","chromium.swiron",18],
        ["Comodo Dragon","chromium.comododragon",16],
        ["Epic Privacy\nBrowser","chromium.epic",14],
        ["Opera GX","chromium.operagx",18],
        ["Opera","chromium.opera",20],
        ["Yandex","chromium.yandex",20],
        ["Arc","chromium.arc",22]
    ],
    "Gaming": [
        ["Legcord","utility.legcord",20],
        ["Discord","utility.discord",20],
        ["Vencord","utility.vencord",20],
        ["Steam","utility.steam",22],
        ["BakkesMod","utility.bakkesmod",20]
    ],
    "Utilities": [
        ["Mullvad VPN","utility.mullvadvpn",18],
        ["Malwarebytes","utility.mwb",18],
        ["Bleachbit","utility.bleachbit",19],
        ["qBittorrent","utility.qbt",18],
        ["Free Download\nManager","utility.fdm",16],
        ["CapFrameX","utility.cfx",18]
    ],
    "Media": [
        ["VLC","utility.vlc",22],
        ["OBS Studio","utility.obs",18],
        ["SoundSwitch","utility.soundswitch",18],
        ["Lightshot","utility.lightshot",19],
        ["ShareX","utility.sharex",20]
    ],
    "Customisation": [
        ["Rainmeter","utility.rainmeter",19],
        ["Windhawk","utility.windhawk",18],
        ["StartAllBack","utility.startallback",16]
    ],
    "Text Editors": [
        ["Visual Studio Code","utility.vscode",14],
        ["Notepad++","utility.nppp",20],
        ["Sublime Text","utility.sublimetext",18],
        ["Atom","utility.atom",22]
    ],
    "Hardware Tools": [
        ["CPU-Z","utility.cpuz",22],
        ["GPU-Z","utility.gpuz",22],
        ["ASRock Timing\nConfigurator","utility.asrocktc",13],
        ["Custom Resolution\nUtility","utility.cru",14],
        ["MoreClockTool","utility.mct",17],
        ["Display Driver\nUninstaller","utility.ddu",16]
    ],
    "System Tools": [
        ["Process Lasso","utility.processlasso",17],
        ["Revo Uninstaller","utility.revouninstaller",15],
        ["WinRAR","utility.winrar",20],
        ["Powershell 7","utility.powershell",18],
        ["Teracopy","utility.teracopy",20],
        ["Everything\nSearch","utility.everything",16]
    ]
}

import customtkinter as ctk
import threading
import asyncio
import aiohttp
import importlib
import ssl
from utils import resource_path
ssl_ctx = ssl.create_default_context(cafile=resource_path("dependencies\\cacert.pem"))

class downloadsPage(ctk.CTkFrame):
    async def completeDownload(self,progressbar,appFrame,msg="Complete", text_color="#55ff55"):
        completeLabel = ctk.CTkLabel(appFrame, text=msg, text_color=text_color, font=ctk.CTkFont(size=20))
        self.master.master.shrink(completeLabel,progressbar.winfo_width(),20)
        self.after(0,progressbar.destroy)
        completeLabel.grid(row=0,column=1,padx=(0,8))
        if msg == "Error":
            await asyncio.sleep(3)
            self.after(0,completeLabel.destroy)
            print(f"attempting to resummon {appFrame.application[1]}")
            btn = ctk.CTkButton(appFrame, text="Download", width=round(appFrame.winfo_width()/4), font=ctk.CTkFont(size=16))
            btn.configure(command=lambda: self.download(btn,appFrame,appFrame.application[1]))
            self.master.master.shrink(btn,round(appFrame.winfo_width()/4),size=16)
            btn.grid(row=0,column=1,padx=(0,5),sticky="e")
    async def procedureWorker(self,app,btn):
        p = importlib.import_module(f"downloads.{app[1]}")
        await p.getURL(self,btn,app[1])
    def download(self,btn,appFrame,name):
        progressbar = ctk.CTkProgressBar(appFrame,width=btn.winfo_width())
        self.after(0,btn.destroy)
        progressbar.set(0)
        app = importlib.import_module(f"downloads.{name}")
        progressbar.grid(row=0,column=1,padx=(0,5),sticky="e")

        async def async_download(url,path,progressbar):
            print(f"attempting to download from {url} to {path}")
            lastUpdateFrac = 0
            async def write(f,chunk):
                nonlocal lastUpdateFrac
                f.write(chunk)
                if total:
                    frac = downloaded/total
                    if frac-lastUpdateFrac >= 0.01 and frac <= 1: #only update ui every 1% downloaded
                        threading.Thread(target=lambda: self.after(0,progressbar.set,frac), daemon=True).start()
                        lastUpdateFrac = frac
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url,ssl=ssl_ctx) as resp:
                        resp.raise_for_status()
                        total = resp.content_length or 0
                        downloaded = 0
                        with open(path, "wb") as f:
                            async for chunk in resp.content.iter_chunked(8192):
                                downloaded += len(chunk)
                                await write(f,chunk)
            except Exception as e:
                print(f"Error during download: {e}")
                await self.completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
                return
            self.after(0,lambda: asyncio.run(self.completeDownload(progressbar,progressbar.master)))
        async def continuation(url,path):
            threading.Thread(target=lambda: asyncio.run(async_download(url,path,progressbar)), daemon=True).start()
        threading.Thread(target=lambda: asyncio.run(app.getURL(ssl_ctx,continuation,progressbar,self.completeDownload)), daemon=True).start()
        
    def __init__(self, master):
        super().__init__(master=master.main_area, fg_color="transparent")
        self.titleBar = ctk.CTkLabel(self, text="Downloads (downloads go to downloads folder)", font=ctk.CTkFont(size=32,weight="bold"), bg_color="#1d1a23", height=50)
        master.shrink(self.titleBar,round(master.width/1250*1020),32)
        self.titleBar.pack(side="top", fill="x", pady=(0,5))
        shrink = master.shrink

        self.scrollableDlFrame = ctk.CTkScrollableFrame(self, fg_color="#201d26")
        for category,applications in downloads.items():
            categoryFrame = ctk.CTkFrame(self.scrollableDlFrame, fg_color="transparent")

            categoryTitle = ctk.CTkLabel(categoryFrame, text=category + "\n──────────────────────────", font=ctk.CTkFont(size=21))
            categoryTitle.grid(row=0, column=0, pady=(0,5), columnspan=5)
            
            w = round((master.width-master.sb.winfo_width()-100)/4)
            print(f"allowing download width of {w}")
            for index,app in enumerate(applications):
                row = index // 4 + 1
                column = index % 4
                appFrame = ctk.CTkFrame(categoryFrame,height=40,width=w)
                appFrame.application = app
                appFrame.grid_propagate(False)

                appFrame.grid_columnconfigure(0, weight=1)  # space for label
                appFrame.grid_columnconfigure(1, weight=0)  # button column
                appFrame.grid_rowconfigure(0, weight=1)  # button column

                isProcedure = True if app[0].startswith("$x") else False
                
                appNameLabel = ctk.CTkLabel(appFrame, text=app[0] if not isProcedure else app[0][2:], font=ctk.CTkFont(size=app[2]), text_color="#ffff00" if app[0].startswith("⭐") else "#ffffff")
                shrink(appNameLabel,round(w/4*3)-20,app[2])
                appDownloadButton = ctk.CTkButton(appFrame, text="Download", width=round(w/4), font=ctk.CTkFont(size=16))
                shrink(appDownloadButton,round(w/4),size=16)
                if isProcedure:
                    appDownloadButton.configure(command=lambda app=app, btn=appDownloadButton: threading.Thread(target=lambda: asyncio.run(self.procedureWorker(app,btn)), daemon=True).start())
                else:
                    appDownloadButton.configure(command=lambda app=app, btn=appDownloadButton: self.download(btn,btn.master,app[1]))
                appNameLabel.grid(row=0,column=0,sticky="ew")
                appDownloadButton.grid(row=0,column=1,padx=(0,5),sticky="e")
                appFrame.grid(row=row,column=column,padx=5,pady=5)
            categoryFrame.pack(pady=10)
        self.scrollableDlFrame.pack(side="top",fill="both",expand=True)
