import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://ungoogled-software.github.io/ungoogled-chromium-binaries/releases/windows/64bit/") as resp:
            resp.raise_for_status()
            html = await resp.text()
    soup = BeautifulSoup(html,"html.parser")
    top_li = soup.find("ul").find("li")
    v = top_li.find("a")["href"].rsplit("/",1)[1]
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://ungoogled-software.github.io/ungoogled-chromium-binaries/releases/windows/64bit/{v}") as resp:
            resp.raise_for_status()
            html = (await resp.text()).split("<h2>Downloads</h2>")[1]
    soup = BeautifulSoup(html,"html.parser")
    top_li = soup.find("ul").find("li")
    url = top_li.find("a")["href"]
    download_path = Path.home() / "Downloads" / url.rsplit("/",1)[1]
    return url,download_path