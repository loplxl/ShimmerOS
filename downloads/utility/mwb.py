from pathlib import Path
async def getURL():
    return "https://downloads.malwarebytes.com/file/mb-windows",(Path.home() / "Downloads" / "MBSetup.exe")