from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://ramensoftware.com/downloads/windhawk_setup.exe",(Path.home() / "Downloads" / "windhawk_setup.exe"))