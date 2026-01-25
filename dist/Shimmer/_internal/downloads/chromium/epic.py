from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://cdn.epicbrowser.com/winsetup/EpicSetup.exe",(Path.home() / "Downloads" / "EpicSetup.exe"))