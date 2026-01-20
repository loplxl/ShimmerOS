import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.torproject.org/download/") as resp:
            resp.raise_for_status()
            html = await resp.text()
    soup = BeautifulSoup(html,"html.parser")
    url = soup.find("a",class_="btn btn-primary mt-4 downloadLink")['href']
    download_path = Path.home() / "Downloads" / url.rsplit("/",1)[1]
    return "https://www.torproject.org" + url,download_path