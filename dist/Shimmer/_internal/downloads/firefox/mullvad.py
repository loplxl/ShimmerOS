from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://mullvad.net/en/download/browser/win64/latest",(Path.home() / "Downloads" / "mullvad-browser-windows-x86_64.exe"))