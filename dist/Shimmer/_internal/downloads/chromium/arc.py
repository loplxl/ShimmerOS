from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://releases.arc.net/windows/ArcInstaller.exe",(Path.home() / "Downloads" / "ArcInstaller.exe"))