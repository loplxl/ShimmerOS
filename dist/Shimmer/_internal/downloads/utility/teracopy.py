from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://www.codesector.com/files/teracopy.exe",(Path.home() / "Downloads" / "teracopy.exe"))