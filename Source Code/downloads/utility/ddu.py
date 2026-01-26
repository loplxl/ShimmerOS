import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.wagnardsoft.com/",ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                html = await resp.text()
        soup = BeautifulSoup(html,"html.parser")
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    for tag in soup.find_all("h5"):
        text = tag.get_text(strip=True)
        if "Download Display Driver Uninstaller" in text:
            version = text.split()[-1]
    url = f"https://www.wagnardsoft.com/DDU/download/DDU%20v{version}.exe"
    download_path = Path.home() / "Downloads" / url.rsplit("/",1)[1]
    await continuation(url,download_path)