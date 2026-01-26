from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://files2.freedownloadmanager.org/6/latest/fdm_x64_setup.exe",(Path.home() / "Downloads" / "fdm_x64_setup.exe"))