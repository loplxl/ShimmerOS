from pathlib import Path
async def getURL():
    return "https://releases.arc.net/windows/ArcInstaller.exe",(Path.home() / "Downloads" / "ArcInstaller.exe")