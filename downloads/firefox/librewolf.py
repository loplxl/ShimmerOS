import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://librewolf.net/installation/windows/") as resp:
            resp.raise_for_status()
            html = await resp.text()
    soup = BeautifulSoup(html,"html.parser")
    url = soup.select_one("a.button.text-gray.focus\\:ring.primary")["href"]
    download_path = Path.home() / "Downloads" / url.rsplit("/",1)[1]
    return url,download_path