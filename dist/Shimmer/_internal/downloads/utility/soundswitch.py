import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://github.com/Belphemur/SoundSwitch/releases/latest", allow_redirects=True,ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                html = await resp.text()
                redirecturl = str(resp.url)
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    tag = redirecturl.rsplit("/tag/",1)[1]
    soup = BeautifulSoup(html,"html.parser")
    links = soup.find_all("a", href=True)
    for link in links:
        if "installer" in link.text.lower() and ".exe" in link.text.lower():
            break
    downloadName = link.text
    url = f"https://github.com/Belphemur/SoundSwitch/releases/download/{tag}/{downloadName}"
    download_path = Path.home() / "Downloads" / link.text
    await continuation(url,download_path)