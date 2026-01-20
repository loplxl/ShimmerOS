from pathlib import Path
async def getURL():
    return "https://browser.yandex.com/download?os=win&bitness=64",(Path.home() / "Downloads" / "Yandex.exe")