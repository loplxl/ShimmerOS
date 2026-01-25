import customtkinter as ctk
import threading
import asyncio
import aiohttp
import importlib
#goal:
#function to delete button, create progressbar and then run the function to get the url
#asynchronously run another function to download it to allow the rest of the gui to work
import ssl
from utils import resource_path
ssl_ctx = ssl.create_default_context(
    cafile=resource_path("dependencies\\cacert.pem")
)

class downloadsPage(ctk.CTkFrame):
    async def completeDownload(self,progressbar,appFrame,msg="Complete", text_color="#55ff55"):
        progressbar.grid_forget()
        completeLabel = ctk.CTkLabel(appFrame, text=msg, text_color=text_color, font=ctk.CTkFont(size=20))
        completeLabel.grid(row=0,column=1,padx=(0,8))
    async def procedureWorker(self,app,btn):
        p = importlib.import_module(f"downloads.{app[1]}")
        await p.getURL(self,btn)
    def download(self,btn,appFrame,name):
        btn.grid_forget()
        progressbar = ctk.CTkProgressBar(appFrame,width=75)
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
                ["Revo Uninstaller","utility.revouninstaller",15],
                ["Visual Studio Code","utility.vscode",14]
            ]
        }
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
            categoryFrame.pack()
        self.scrollableDlFrame.pack(side="top",fill="both",expand=True)
