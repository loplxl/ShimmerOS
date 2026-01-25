from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://www.srware.net/downloads/srware_iron64.exe",(Path.home() / "Downloads" / "srware_iron64.exe"))