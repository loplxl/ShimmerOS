from pathlib import Path
async def getURL():
    return "https://github.com/Vencord/Installer/releases/latest/download/VencordInstaller.exe",(Path.home() / "Downloads" / "VencordInstaller.exe")