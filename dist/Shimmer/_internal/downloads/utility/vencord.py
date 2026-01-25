from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://github.com/Vencord/Installer/releases/latest/download/VencordInstaller.exe",(Path.home() / "Downloads" / "VencordInstaller.exe"))