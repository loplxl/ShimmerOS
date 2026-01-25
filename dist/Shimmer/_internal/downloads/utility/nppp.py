import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
import re
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://notepad-plus-plus.org/#main",ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                html = await resp.text()
        soup = BeautifulSoup(html,"html.parser")
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    url = soup.find("p",class_="library-desc").find("a")['href']
    matches = re.findall(r"(\d+\.?)",url)
    version = "".join(matches)
    download_path = Path.home() / "Downloads" / f"npp.{version}.Installer.x64.exe"
    url = f"https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v{version}/npp.{version}.Installer.x64.exe"
    await continuation(url,download_path)