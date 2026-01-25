import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
import re
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://github.com/ShareX/ShareX/releases/latest", allow_redirects=True,ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                redirecturl = str(resp.url)
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    version = redirecturl.rsplit("v",1)[1]
    url = f"https://github.com/ShareX/ShareX/releases/download/v{version}/ShareX-{version}-setup.exe"
    await continuation(url,(Path.home() / "Downloads" / f"ShareX-{version}-setup.exe"))