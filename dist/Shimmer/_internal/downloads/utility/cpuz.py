import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.cpuid.com/softwares/cpu-z.html",ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                html = await resp.text()
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    soup = BeautifulSoup(html,"html.parser")
    url = soup.find("a",class_="button icon-exe")['href']
    name = url.rsplit("/",1)[1]
    download_path = Path.home() / "Downloads" / name
    await continuation("https://download.cpuid.com/cpu-z/" + name,download_path)