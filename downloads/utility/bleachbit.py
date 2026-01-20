import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.bleachbit.org/download/windows") as resp:
            resp.raise_for_status()
            html = await resp.text()
    soup = BeautifulSoup(html,"html.parser")
    url = soup.find("a", href=lambda href: href and "bleachbit" in href.lower() and href.endswith(".exe"))['href']
    filename = url.rsplit("file=",1)[1]
    url = "https://download.bleachbit.org/" + filename
    download_path = Path.home() / "Downloads" / filename
    return url,download_path