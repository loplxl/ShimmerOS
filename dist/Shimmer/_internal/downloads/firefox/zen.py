from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://github.com/zen-browser/desktop/releases/latest/download/zen.installer.exe",(Path.home() / "Downloads" / "zen.installer.exe"))