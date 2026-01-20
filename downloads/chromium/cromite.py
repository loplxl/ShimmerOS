from pathlib import Path
async def getURL():
    return "https://github.com/uazo/cromite/releases/latest/download/chrome-win.zip",(Path.home() / "Downloads" / "cromite-chrome-win.zip")