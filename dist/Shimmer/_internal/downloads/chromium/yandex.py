from pathlib import Path
async def getURL(ssl_ctx,continuation,progressbar,completeDownload):
    await continuation("https://browser.yandex.com/download?os=win&bitness=64",(Path.home() / "Downloads" / "Yandex.exe"))