from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://downloads.malwarebytes.com/file/mb-windows",(Path.home() / "Downloads" / "MBSetup.exe"))