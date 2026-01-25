import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.waterfox.com/download/",ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                html = await resp.text()
        soup = BeautifulSoup(html,"html.parser")
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    url = soup.find("a",class_="flex h-13 w-full items-center justify-between px-4 text-left transition-colors hover:bg-accent")['href']
    download_path = Path.home() / "Downloads" / url.rsplit("/",1)[1].replace("%20",' ')
    await continuation(url,download_path)