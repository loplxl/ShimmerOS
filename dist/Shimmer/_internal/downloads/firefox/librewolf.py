import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://librewolf.net/installation/windows/",ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                html = await resp.text()
        soup = BeautifulSoup(html,"html.parser")
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    url = soup.select_one("a.button.text-gray.focus\\:ring.primary")["href"]
    download_path = Path.home() / "Downloads" / url.rsplit("/",1)[1]
    await continuation(url,download_path)