from pathlib import Path
async def getURL():
    return "https://github.com/Floorp-Projects/Floorp/releases/latest/download/floorp-windows-x86_64.installer.exe",(Path.home() / "Downloads" / "floorp-windows-x86_64.installer.exe")