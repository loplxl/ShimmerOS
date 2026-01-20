import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.waterfox.com/download/") as resp:
            resp.raise_for_status()
            html = await resp.text()
    soup = BeautifulSoup(html,"html.parser")
    url = soup.find("a",class_="flex h-13 w-full items-center justify-between px-4 text-left transition-colors hover:bg-accent")['href']
    download_path = Path.home() / "Downloads" / url.rsplit("/",1)[1].replace("%20",' ')
    return url,download_path