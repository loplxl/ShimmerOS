from pathlib import Path
async def getURL():
    return "https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US",(Path.home() / "Downloads" / "Firefox Installer.exe")