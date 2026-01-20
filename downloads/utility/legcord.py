import aiohttp
from pathlib import Path
async def getURL():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://github.com/Legcord/Legcord/releases/latest", allow_redirects=True) as resp:
            resp.raise_for_status()
            redirecturl = str(resp.url)
    version = redirecturl.rsplit("v",1)[1]
    url = f"https://github.com/Legcord/Legcord/releases/download/v{version}/Legcord-{version}-win-x64.exe"
    return url,(Path.home() / "Downloads" / f"Legcord-{version}-win-x64.exe")