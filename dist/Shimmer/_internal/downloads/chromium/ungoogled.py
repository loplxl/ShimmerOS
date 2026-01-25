import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://ungoogled-software.github.io/ungoogled-chromium-binaries/releases/windows/64bit/",ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                html = await resp.text()
        soup = BeautifulSoup(html,"html.parser")
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    top_li = soup.find("ul").find("li")
    v = top_li.find("a")["href"].rsplit("/",1)[1]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://ungoogled-software.github.io/ungoogled-chromium-binaries/releases/windows/64bit/{v}",ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                html = (await resp.text()).split("<h2>Downloads</h2>")[1]
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    soup = BeautifulSoup(html,"html.parser")
    top_li = soup.find("ul").find("li")
    url = top_li.find("a")["href"]
    download_path = Path.home() / "Downloads" / url.rsplit("/",1)[1]
    await continuation(url,download_path)