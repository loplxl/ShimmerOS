from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://app.prntscr.com/build/setup-lightshot.exe",(Path.home() / "Downloads" / "setup-lightshot.exe"))