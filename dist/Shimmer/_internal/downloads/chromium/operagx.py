from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://net.geo.opera.com/opera_gx/stable/windows",(Path.home() / "Downloads" / "OperaGXSetup.exe"))