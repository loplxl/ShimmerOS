from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://www.autohotkey.com/download/ahk-install.exe",(Path.home() / "Downloads" / "ahk-install.exe"))