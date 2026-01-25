from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://github.com/Floorp-Projects/Floorp/releases/latest/download/floorp-windows-x86_64.installer.exe",(Path.home() / "Downloads" / "floorp-windows-x86_64.installer.exe"))