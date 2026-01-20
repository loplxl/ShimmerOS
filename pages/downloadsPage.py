import customtkinter as ctk
import threading
import asyncio
import aiohttp
import importlib
#goal:
#function to delete button, create progressbar and then run the function to get the url
#asynchronously run another function to download it to allow the rest of the gui to work

class downloadsPage(ctk.CTkFrame):
    async def uiUpdate(self,progressbar,frac):
        print("ui update called")
        progressbar.set(frac)
    def completeDownload(self,progressbar,appFrame):
        completeLabel = ctk.CTkLabel(appFrame, text="Complete", text_color="#00ff00", font=ctk.CTkFont(size=20))
        progressbar.destroy()
        completeLabel.grid(row=0,column=1,padx=(0,8))
    def download(self,btn,appFrame,name):
        btn.destroy()
        progressbar = ctk.CTkProgressBar(appFrame,width=75)
        progressbar.set(0)
        app = importlib.import_module(f"downloads.{name}")
        progressbar.grid(row=0,column=1,padx=(0,5),sticky="e")
        url,path = asyncio.run(app.getURL())
        async def uiUpdate(progressbar,frac):
            self.after(0,progressbar.set,frac)
        async def async_download(url,path,progressbar):
            lastUpdateFrac = 0
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    total = resp.content_length or 0
                    downloaded = 0
                    with open(path, "wb") as f:
                        async for chunk in resp.content.iter_chunked(8192):
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total:
                                frac = downloaded/total
                                if frac-lastUpdateFrac >= 0.01: #only update ui every 1% downloaded
                                    threading.Thread(target=lambda: asyncio.run(uiUpdate(progressbar,frac)), daemon=True).start() #asynchronous download
                                    lastUpdateFrac = frac

            self.after(0,lambda: self.completeDownload(progressbar,progressbar.master))
        threading.Thread(target=lambda: asyncio.run(async_download(url,path,progressbar)), daemon=True).start() #asynchronous download


        
    def __init__(self, master):
        super().__init__(master=master.main_area, fg_color="transparent")
        self.titleBar = ctk.CTkLabel(self, text="Downloads (downloads go to downloads folder)", font=ctk.CTkFont(size=32,weight="bold"), bg_color="#1d1a23", height=50)
        self.titleBar.pack(side="top", fill="x", pady=(0,5))
        downloads = { #category / [name to display,module location,font size]
            "Oslivion Options quick access": [
                ["Autoruns","quickaccess.autoruns",20],
                ["GoInterruptPolicy","quickaccess.goip",18]
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
            "Utilities": [
                ["Legcord","utility.legcord",20],
                ["Discord","utility.discord",20],
                ["Vencord","utility.vencord",20],
                ["Steam","utility.steam",22],
                ["VLC","utility.vlc",22],
                ["Custom Resolution\nUtility","utility.cru",14],
                ["MoreClockTool","utility.mct",17],
                ["CPU-Z","utility.cpuz",22],
                ["Notepad++","utility.nppp",20],
                ["Powershell 7","utility.powershell",18],
                ["Mullvad VPN","utility.mullvadvpn",18],
                ["Teracopy","utility.teracopy",20],
                ["SoundSwitch","utility.soundswitch",18],
                ["Lightshot","utility.lightshot",19],
                ["ShareX","utility.sharex",20],
                ["Everything\nSearch","utility.everything",16],
                ["OBS Studio","utility.obs",18],
                ["Rainmeter","utility.rainmeter",19],
                ["WinRAR","utility.winrar",20],
                ["Malwarebytes","utility.mwb",18],
                ["Bleachbit","utility.bleachbit",19],
                ["Process Lasso","utility.processlasso",17],
                ["Revo Uninstaller","utility.revouninstaller",15]
            ]
        }
        self.scrollableDlFrame = ctk.CTkScrollableFrame(self, fg_color="#201d26")
        for category,applications in downloads.items():
            categoryFrame = ctk.CTkFrame(self.scrollableDlFrame, fg_color="transparent")

            categoryTitle = ctk.CTkLabel(categoryFrame, text=category + "\n──────────────────────────────", font=ctk.CTkFont(size=24))
            categoryTitle.grid(row=0, column=0, pady=(0,5), columnspan=5)
            
            for index,app in enumerate(applications):
                row = index // 4 + 1
                column = index % 4
                appFrame = ctk.CTkFrame(categoryFrame)
                appFrame.grid_propagate(False)
                appFrame.configure(height=40,width=220)

                appFrame.grid_columnconfigure(0, weight=1)  # space for label
                appFrame.grid_columnconfigure(1, weight=0)  # button column
                appFrame.grid_rowconfigure(0, weight=1)  # button column

                appNameLabel = ctk.CTkLabel(appFrame, text=app[0], font=ctk.CTkFont(size=app[2]), text_color="#ffff00" if app[0].startswith("⭐") else "#ffffff")
                appDownloadButton = ctk.CTkButton(appFrame, text="Download", width=90, font=ctk.CTkFont(size=16))
                appDownloadButton.configure(command=lambda app=app, btn=appDownloadButton: self.download(btn,btn.master,app[1]))
                appNameLabel.grid(row=0,column=0,sticky="ew")
                appDownloadButton.grid(row=0,column=1,padx=(0,5),sticky="e")
                appFrame.grid(row=row,column=column,padx=5,pady=5,sticky="ew")
            categoryFrame.pack()
        self.scrollableDlFrame.pack(side="top",fill="both",expand=True)