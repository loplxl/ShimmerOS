import aiohttp
from pathlib import Path
async def getURL():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://github.com/obsproject/obs-studio/releases/latest", allow_redirects=True) as resp:
            resp.raise_for_status()
            redirecturl = str(resp.url)
    version = redirecturl.rsplit("/",1)[1]
    url = f"https://github.com/obsproject/obs-studio/releases/download/{version}/OBS-Studio-{version}-Windows-x64-Installer.exe"
    return url,(Path.home() / "Downloads" / f"OBS-Studio-{version}-Windows-x64-Installer.exe")