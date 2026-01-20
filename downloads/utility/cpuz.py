import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.cpuid.com/softwares/cpu-z.html") as resp:
            resp.raise_for_status()
            html = await resp.text()
    soup = BeautifulSoup(html,"html.parser")
    url = soup.find("a",class_="button icon-exe")['href']
    name = url.rsplit("/",1)[1]
    download_path = Path.home() / "Downloads" / name
    return "https://download.cpuid.com/cpu-z/" + name,download_path