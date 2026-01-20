import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://customresolutionutility.net/") as resp:
            resp.raise_for_status()
            html = await resp.text()
    soup = BeautifulSoup(html,"html.parser")
    url = soup.find("figure",class_="wp-block-table").find("a")["href"]
    print(url)
    download_path = Path.home() / "Downloads" / url.rsplit("/",1)[1]
    return url,download_path