from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://dl.google.com/chrome/install/ChromeStandaloneSetup64.exe",(Path.home() / "Downloads" / "ChromeStandaloneSetup64.exe"))