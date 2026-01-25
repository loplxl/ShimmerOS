import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.bleachbit.org/download/windows",ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                html = await resp.text()
        soup = BeautifulSoup(html,"html.parser")
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    url = soup.find("a", href=lambda href: href and "bleachbit" in href.lower() and href.endswith(".exe"))['href']
    filename = url.rsplit("file=",1)[1]
    url = "https://download.bleachbit.org/" + filename
    download_path = Path.home() / "Downloads" / filename
    await continuation(url,download_path)