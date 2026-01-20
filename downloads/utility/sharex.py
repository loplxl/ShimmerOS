import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
import re
async def getURL():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://github.com/ShareX/ShareX/releases/latest", allow_redirects=True) as resp:
            resp.raise_for_status()
            redirecturl = str(resp.url)
    version = redirecturl.rsplit("v",1)[1]
    url = f"https://github.com/ShareX/ShareX/releases/download/v{version}/ShareX-{version}-setup.exe"
    return url,(Path.home() / "Downloads" / f"ShareX-{version}-setup.exe")