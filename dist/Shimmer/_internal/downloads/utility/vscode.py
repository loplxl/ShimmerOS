from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user",(Path.home() / "Downloads" / "VSCodeUserSetup-x64.exe"))