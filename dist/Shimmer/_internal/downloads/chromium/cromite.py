from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://github.com/uazo/cromite/releases/latest/download/chrome-win.zip",(Path.home() / "Downloads" / "cromite-chrome-win.zip"))