from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://download.revouninstaller.com/download/revosetup.exe",(Path.home() / "Downloads" / "revosetup.exe"))