from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://github.com/atom/atom/releases/latest/download/AtomSetup-x64.exe",(Path.home() / "Downloads" / "AtomSetup-x64.exe"))