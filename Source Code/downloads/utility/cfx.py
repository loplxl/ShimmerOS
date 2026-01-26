import aiohttp
from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://github.com/CXWorld/CapFrameX/releases/latest", allow_redirects=True,ssl=ssl_ctx) as resp:
                resp.raise_for_status()
                redirecturl = str(resp.url)
        version = redirecturl.rsplit("v",1)[1]
    except Exception as e:
        print(f"Error during download: {e}")
        await completeDownload(progressbar,progressbar.master,msg="Error",text_color="#ff5555")
        return
    url = f"https://github.com/CXWorld/CapFrameX/releases/latest/download/release_{version}_installer.zip/"
    await continuation(url,(Path.home() / "Downloads" / f"CapFrameX_release_{version}_installer.zip"))