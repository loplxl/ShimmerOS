from pathlib import Path
async def getURL():
    return "https://github.com/brave/brave-browser/releases/latest/download/BraveBrowserStandaloneSetup.exe",(Path.home() / "Downloads" / "BraveBrowserStandaloneSetup.exe")