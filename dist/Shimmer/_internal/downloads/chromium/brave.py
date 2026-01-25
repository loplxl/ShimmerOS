from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://github.com/brave/brave-browser/releases/latest/download/BraveBrowserStandaloneSetup.exe",(Path.home() / "Downloads" / "BraveBrowserStandaloneSetup.exe"))