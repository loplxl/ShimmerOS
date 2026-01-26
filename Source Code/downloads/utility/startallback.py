from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://www.startallback.com/download.php",(Path.home() / "Downloads" / "StartAllBack_setup.exe"))