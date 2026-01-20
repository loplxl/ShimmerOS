import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
import re
async def getURL():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://github.com/imputnet/helium-windows/releases/latest") as resp:
            resp.raise_for_status()
            html = await resp.text()
    soup = BeautifulSoup(html,"html.parser")
    matches = re.findall(r"(\d+\.?)",soup.find("title").get_text())
    version = "".join(matches)
    url = f"https://github.com/imputnet/helium-windows/releases/download/{version}/helium_{version}_x64-installer.exe"
    
    return url,(Path.home() / "Downloads" / f"helium_{version}_x64-installer.exe")