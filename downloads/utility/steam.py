from pathlib import Path
async def getURL():
    return "https://cdn.fastly.steamstatic.com/client/installer/SteamSetup.exe",(Path.home() / "Downloads" / "SteamSetup.exe")