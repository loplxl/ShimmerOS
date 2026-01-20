import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
async def getURL():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://github.com/Belphemur/SoundSwitch/releases/latest", allow_redirects=True) as resp:
            resp.raise_for_status()
            html = await resp.text()
            redirecturl = str(resp.url)
    tag = redirecturl.rsplit("/tag/",1)[1]
    soup = BeautifulSoup(html,"html.parser")
    links = soup.find_all("a", href=True)
    for link in links:
        if "installer" in link.text.lower() and ".exe" in link.text.lower():
            break
    downloadName = link.text
    url = f"https://github.com/Belphemur/SoundSwitch/releases/download/{tag}/{downloadName}"
    download_path = Path.home() / "Downloads" / link.text
    return url,download_path