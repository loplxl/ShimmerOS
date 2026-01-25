import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
import re
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://github.com/imputnet/helium-windows/releases/latest",ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                html = await resp.text()
        soup = BeautifulSoup(html,"html.parser")
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    matches = re.findall(r"(\d+\.?)",soup.find("title").get_text())
    version = "".join(matches)
    url = f"https://github.com/imputnet/helium-windows/releases/download/{version}/helium_{version}_x64-installer.exe"

    await continuation(url,(Path.home() / "Downloads" / f"helium_{version}_x64-installer.exe"))